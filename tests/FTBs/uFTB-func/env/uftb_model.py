import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from mlvp.modules import PLRU, TwoBitsCounter
from mlvp import *
from drivers.ftb_way import *
from drivers.config import *

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
        self.ubtb_enable = 1
        self.meta = [(0, None), (0, None), (0, None)]

        self.pred_result_ftb_entry = None
        self.pred_result_br_taken_mask = None
        self.pred_result_meta = None

        # Update requests are used to update FTBways and counters.
        self.update_queue = []

        # The update queue of the replacement algorithm, and there are two channels,
        # the first channel has a higher priority.
        self.replacer_update_queue = [[], []]

    def update(self, update_request):
        self.update_queue.append((update_request, 2, None))

    def generate_output(self, s0_fire, s0_pc):
        if not self.ubtb_enable:
            return None, None, None
        if s0_fire:
            hit_way = self._find_hit_way(s0_pc)
            if hit_way is not None:
                # self.replacer_update_queue[0].append((hit_way, 1))

                self.pred_result_ftb_entry = self.ftbways[hit_way].ftb_entry
                self.pred_result_br_taken_mask = self._generate_br_taken_mask(hit_way)
            else:
                self.pred_result_ftb_entry = None
                self.pred_result_br_taken_mask = None
            
            self.meta[0] = self.meta[1]
            self.meta[1] = self.meta[2]
            self.meta[2] = (hit_way, hit_way is not None)

            if self.meta[0] is not None and self.meta[0][1]:
                self.pred_result_meta = self.meta[0][0]
                return self.pred_result_ftb_entry, self.pred_result_br_taken_mask, self.pred_result_meta
            else:
                self.pred_result_meta = self.meta[0][0]
                return self.pred_result_ftb_entry, self.pred_result_br_taken_mask, self.pred_result_meta
        else:
            return self.pred_result_ftb_entry, self.pred_result_br_taken_mask, self.pred_result_meta

    def print_all_ftb_ways(self):
        for i in range(UFTB_WAYS_NUM):
            if not self.ftbways[i].valid:
                continue
            co1 = self.counters[i][0].counter
            co2 = self.counters[i][1].counter
            info(f"way {i}: valid: {self.ftbways[i].valid}, tag: {hex(self.ftbways[i].tag << 1)}, [{co1}, {co2}]")

    def _generate_br_taken_mask(self, hit_way):
        ftb_entry = self.ftbways[hit_way].ftb_entry
        br_taken_mask = [self.counters[hit_way][0].get_prediction(), 
                         self.counters[hit_way][1].get_prediction()]
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
                self.update_queue[i] = (self.update_queue[i][0], 
                                        self.update_queue[i][1], 
                                        selected_way)
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

                new_update_queue.append((self.update_queue[i][0], 
                                         self.update_queue[i][1] - 1, 
                                         selected_way))
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

        need_to_update[0] = update_request["ftb_entry"]["brSlots_0_valid"] and \
                            update_request["valid"] and \
                            not update_request["ftb_entry"]["always_taken_0"]
        
        need_to_update[1] = update_request["ftb_entry"]["tailSlot_valid"] and \
                            update_request["ftb_entry"]["tailSlot_sharing"] and \
                            update_request["valid"] and \
                            not update_request["ftb_entry"]["always_taken_1"] and \
                            not update_request["bits_br_taken_mask_0"]

        if need_to_update[0]:
            self.counters[selected_way][0].update(update_request["bits_br_taken_mask_0"])
        if need_to_update[1]:
            self.counters[selected_way][1].update(update_request["bits_br_taken_mask_1"])

    def _update_all(self, update_request, selected_way):
        self._update_ftb_ways(update_request, selected_way)
        self._update_counters(update_request, selected_way)

