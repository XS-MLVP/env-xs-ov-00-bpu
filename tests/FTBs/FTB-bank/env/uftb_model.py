from mlvp.modules import PLRU, TwoBitsCounter
from mlvp import *

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from drivers.ftb_way import *

class uFTBWay:
    def __init__(self):
        self.valid = 0
        self.tag = 0
        self.ftb_entry = FTBEntry()

    @staticmethod
    def get_tag(pc):
        return pc >> INST_OFFSET_BITS & ((1 << UFTB_TAG_SIZE) - 1)

class uFTBModel:
    def __init__(self):
        self.replacer = PLRU(UFTB_WAYS_NUM)
        self.ftbways = [uFTBWay() for _ in range(UFTB_WAYS_NUM)]
        self.counters = [[TwoBitsCounter(), TwoBitsCounter()] for _ in range(UFTB_WAYS_NUM)]

        # Update requests are used to update FTBways and counters.
        self.update_queue = []

        # The update queue of the replacement algorithm, and there are two channels,
        # the first channel has a higher priority.
        self.replacer_update_queue = [[], []]

    def update(self, update_request):
        self.update_queue.append((update_request, 2, None))

    def generate_output(self, s1_fire, s1_pc):
        self._process_update()
        if s1_fire:
            hit_way = self._find_hit_way(s1_pc)
            if hit_way is None:
                return None
            self.replacer_update_queue[0].append((hit_way, 1))

            ftb_entry = self.ftbways[hit_way].ftb_entry
            br_taken_mask = self._generate_br_taken_mask(hit_way)

            return ftb_entry, br_taken_mask, hit_way

    def print_all_ftb_ways(self):
        for i in range(UFTB_WAYS_NUM):
            debug(f"way {i}: valid: {self.ftbways[i].valid}, tag: {hex(self.ftbways[i].tag << 1)}")

    def _generate_br_taken_mask(self, hit_way):
        ftb_entry = self.ftbways[hit_way].ftb_entry
        br_taken_mask = [self.counters[hit_way][0].get_prediction(), self.counters[hit_way][1].get_prediction()]
        for i in range(2):
            if ftb_entry.always_taken[i]:
                br_taken_mask[i] = 1
        return br_taken_mask

    def _process_update(self):
        # Update replacement algorithm
        for i in range(2):
            new_update_queue = []
            for j in range(len(self.replacer_update_queue[i])):
                if self.replacer_update_queue[i][j][1] == 0:
                    self.replacer.update(self.replacer_update_queue[i][j][0])
                else:
                    new_update_queue.append((self.replacer_update_queue[i][j][0], self.replacer_update_queue[i][j][1] - 1))
            self.replacer_update_queue[i] = new_update_queue

        # Processing update requests

        # Find the item for the next cycle update to fit the dut hit mode
        next_cycle_update_item = []
        for i in range(len(self.update_queue)):
            selected_way = self.update_queue[i][2]
            if self.update_queue[i][1] == 1:
                if selected_way is None:
                    selected_way = self.replacer.get()
                next_cycle_update_item.append((self.update_queue[i][0], selected_way))
                self.update_queue[i] = (self.update_queue[i][0], self.update_queue[i][1], selected_way)
                self.replacer_update_queue[1].insert(0, (selected_way, 0))

        # Update request processing
        new_update_queue = []
        for i in range(len(self.update_queue)):
            if self.update_queue[i][1] == 0:
                self._update_all(self.update_queue[i][0], self.update_queue[i][2])
            else:
                selected_way = self.update_queue[i][2]
                if self.update_queue[i][1] == 2:
                    selected_way = self._find_hit_way(self.update_queue[i][0]['bits_pc'])

                    for (update_request, way) in next_cycle_update_item:
                        if uFTBWay.get_tag(self.update_queue[i][0]['bits_pc']) == uFTBWay.get_tag(update_request["bits_pc"]):
                            if selected_way is None or way < selected_way:
                                selected_way = way
                                break
                    debug(f"Hit selected way is {selected_way}")

                new_update_queue.append((self.update_queue[i][0], self.update_queue[i][1] - 1, selected_way))
        self.update_queue = new_update_queue

    def _find_hit_way(self, pc):
        tag = uFTBWay.get_tag(pc)
        for i in range(UFTB_WAYS_NUM):
            if self.ftbways[i].valid and self.ftbways[i].tag == tag:
                return i
        return None

    def _update_ftb_ways(self, update_request, selected_way):
        if not update_request["valid"]:
            return

        debug(f"ftb entry {hex(update_request['bits_pc'])} is put into way {selected_way}")
        self.ftbways[selected_way].valid = 1
        self.ftbways[selected_way].tag = uFTBWay.get_tag(update_request["bits_pc"])
        self.ftbways[selected_way].ftb_entry = FTBEntry.from_dict(update_request["ftb_entry"])

    def _update_counters(self, update_request, selected_way):
        if not update_request["valid"]:
            return

        need_to_update = [False, False]
        brslot_valid = [update_request["ftb_entry"]["brSlots_0_valid"], update_request["ftb_entry"]["tailSlot_valid"] and update_request["ftb_entry"]["tailSlot_sharing"]]
        br_taken_mask = [update_request["bits_br_taken_mask_0"], update_request["bits_br_taken_mask_1"]]
        always_taken = [update_request["ftb_entry"]["always_taken_0"], update_request["ftb_entry"]["always_taken_1"]]

        cfi_pos = 0 if br_taken_mask[0] else (1 if br_taken_mask[1] else 2)
        for i in range(2):
            need_to_update[i] = i <= cfi_pos \
                                and not always_taken[i] \
                                and brslot_valid[i]

        for i in range(2):
            if need_to_update[i]:
                self.counters[selected_way][i].update(br_taken_mask[i])

    def _update_all(self, update_request, selected_way):
        self._update_ftb_ways(update_request, selected_way)
        self._update_counters(update_request, selected_way)

