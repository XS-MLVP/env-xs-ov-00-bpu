from mlvp.modules import PLRU, TwoBitsCounter
from mlvp import info, debug
from .ftb_way import *

# pc: | ... |<-- tag(20 bits) -->|<-- idx(9 bits) -->|<-- instOffset(1 bit) -->|
#           |     way number     |    group number   |

class FTBWay:
    def __init__(self):
        self.valid = 0
        self.tag = 0
        self.ftb_entry = FTBEntry()
    
    @staticmethod
    def get_tag(pc):
        return pc >> (INST_OFFSET_BITS + FTB_IDX_BITS) & ((1 << FTB_TAG_BITS) - 1)
    
    def __str__(self, pc) -> str:
        str = ""
        str += f"[FTBEntry] at {hex(pc)}\n"
        str += f"* Slots:\n"
        str += self.brSlot.__str__(pc, True)
        str += self.tailSlot.__str__(pc, self.tailSlot.sharing)
        str += "* Other Info:\n"
        str += f"*\tFallthrough Addr: {hex(get_fallthrough_addr(pc, self.pftAddr, self.carry))}\n"
        str += f"*\tisCall: {self.isCall}, isRet: {self.isRet}, isJalr: {self.isJalr}, isJal: {self.isJal}\n"
        str += f"*\tlast_may_be_rvi_call: {self.last_may_be_rvi_call}, always_taken: {self.always_taken}\n"
        return str

class FTBSet:
    def __init__(self):
        self.ftbways = [FTBWay() for _ in range(FTB_BANK_WAYS_NUM)]
        self.idx = 0
        self.replacer = PLRU(FTB_BANK_WAYS_NUM)
        # self.counters = [[TwoBitsCounter(), TwoBitsCounter()] for _ in range(FTB_BANK_WAYS_NUM)]

    @staticmethod
    def get_idx(pc):
        return pc >> INST_OFFSET_BITS & ((1 << FTB_IDX_BITS) - 1)
    
    def find_way_from_tag(self, tag):
        for i in range(FTB_BANK_WAYS_NUM):
            if self.ftbways[i].valid and self.ftbways[i].tag == tag:
                return i
        return None
    
    def _find_empty_way(self, idx):
        for i in range(FTB_BANK_WAYS_NUM):
            if not self.ftbways[i].valid:
                return i
        return None
    
    # def _update_counters(self, update_request, selected_way):
    #     if not update_request["valid"]:
    #         return

    #     need_to_update = [False, False]
    #     brslot_valid = [update_request["ftb_entry"]["brSlots_0_valid"], 
    #                     update_request["ftb_entry"]["tailSlot_valid"] and 
    #                     update_request["ftb_entry"]["tailSlot_sharing"]]
    #     always_taken = [update_request["ftb_entry"]["always_taken_0"], 
    #                     update_request["ftb_entry"]["always_taken_1"]]

    #     for i in range(2):
    #         need_to_update[i] = not always_taken[i] and brslot_valid[i]

    #     for i in range(2):
    #         if need_to_update[i]:
    #             self.counters[selected_way][i].update(br_taken_mask[i])

class FTBBank:
    def __init__(self):
        self.ftbsets = [FTBSet() for _ in range(FTB_BANK_SETS_NUM)]
        self.update_hits = None
        self.update_access = None
        # self.update_write_alloc = None

        self.update_queue = []
        # self.replacer_update_queue = [[], []]

    def find_set_from_idx(self, idx):
        for i in range(FTB_BANK_SETS_NUM):
            if self.ftbsets[i].idx == idx:
                return i
        return None
    
    def update(self, update_request):
        idx = FTBSet.get_idx(update_request["bits_pc"])
        pc = FTBWay.get_tag(update_request["bits_pc"])
        debug(f"update request [{idx}] {hex(pc)}")
        self.update_queue.append((update_request, 2, None, None))
    
    def generate_output(self, s2_fire, s2_pc): 
        # debug(FTBSet.get_idx(s2_pc))
        debug(f"generate output [{FTBSet.get_idx(s2_pc)}] {hex(FTBWay.get_tag(s2_pc))}")
        # debug(self)

        # self.process_update()

        if not s2_fire:
            return None, None

        read_resp, read_hits = self.process_read(s2_pc)
        if read_hits is None:
            return None
        # self.replacer_update_queue[0].append((s2_pc, read_hits, 2))
        self._update_replacer(FTBSet.get_idx(s2_pc), read_hits)
        # br_taken_mask = self._generate_br_taken_mask(s2_pc, read_hits)

        return read_resp, read_hits
    
    def process_read(self, req_pc):
        # lookup idx and tag
        idx = FTBSet.get_idx(req_pc)
        tag = FTBWay.get_tag(req_pc)

        # find FTBWay
        way = self.ftbsets[idx].find_way_from_tag(tag)
        if way is None:
            return None, None

        # return read_resp(the target FTBway) and read_hits(Which way is hit)
        read_resp = self.ftbsets[idx].ftbways[way].ftb_entry
        read_hits = way
        return read_resp, read_hits

    def process_update(self):
        new_update_queue = []
        for (update_request, clock_cycle, way, update_write_alloc) in self.update_queue:
            pc = update_request["bits_pc"]
            # if clock_cycle == 0:
            #     debug(f"[{FTBSet.get_idx(pc)}] {hex(FTBWay.get_tag(pc))} stage 2")
            #     self._update_write(update_request,
            #                        way, 
            #                        update_write_alloc)
            if clock_cycle == 1:
                debug(f"[{FTBSet.get_idx(pc)}] {hex(FTBWay.get_tag(pc))} stage 1")
                if way is not None:
                    alloc = False
                else:
                    alloc = True
                # new_update_queue.append((update_request, 
                #                             clock_cycle - 1, 
                #                             way,
                #                             alloc))
                self._update_write(update_request,
                                   way, 
                                   alloc)
            elif clock_cycle == 2:
                debug(f"[{FTBSet.get_idx(pc)}] {hex(FTBWay.get_tag(pc))} stage 0")
                meta = parse_uftb_meta(update_request["bits_meta"])
                # debug(meta)
                if meta["hit"]:
                    self._update_ways(FTBSet.get_idx(update_request["bits_pc"]), 
                                      meta["pred_way"], 
                                      update_request["bits_pc"], 
                                      update_request["ftb_entry"])
                    self.update_access = False
                else:
                    self._update_read(update_request["bits_pc"])
                    self.update_access = True
                    new_update_queue.append((update_request, 
                                             clock_cycle - 1, 
                                             self.update_hits,
                                             update_write_alloc))
                
        self.update_queue = new_update_queue
        
    def _update_read(self, u_req_pc):
        idx = FTBSet.get_idx(u_req_pc)
        tag = FTBWay.get_tag(u_req_pc)

        way_index = self.ftbsets[idx].find_way_from_tag(tag)
        if way_index is not None:
            # hit
            self.update_hits = way_index
        else:
            # miss
            self.update_hits = None
        
    def _update_write(self, update_request, update_write_way, update_write_alloc: bool):
        pc = FTBWay.get_tag(update_request["bits_pc"])
        # debug(f"write request {hex(pc)}")
        if not update_request["valid"]:
            return
                
        idx = FTBSet.get_idx(update_request["bits_pc"])

        if update_write_alloc:
            # assign new FTB way
            empty_way = self._find_empty_way(idx)
            if empty_way is not None:
                self._update_ways(idx, empty_way, update_request["bits_pc"], update_request["ftb_entry"])
            else:
                # LRU
                replace_way = self.ftbsets[idx].replacer.get()
                self._update_ways(idx, replace_way, update_request["bits_pc"], update_request["ftb_entry"])
        elif update_request["ftb_entry"] is not None:
            self._update_ways(idx, update_write_way, update_request["bits_pc"], update_request["ftb_entry"])
            
    def _find_empty_way(self, idx):
        for i in range(len(self.ftbsets[idx].ftbways)):
            if self.ftbsets[idx].ftbways[i].valid == 0:
                return i
        return None
    
    def _update_ways(self, idx, way, pc, update_write_data):
        self.ftbsets[idx].ftbways[way].ftb_entry = FTBEntry.from_dict(update_write_data)
        self.ftbsets[idx].ftbways[way].valid = 1
        self.ftbsets[idx].ftbways[way].tag = FTBWay.get_tag(pc)
        self._update_replacer(idx, way)
        debug(f"{hex(FTBWay.get_tag(pc))} is put to [{idx}] [{way}]")

    def _update_replacer(self, idx, way):
        self.ftbsets[idx].replacer.update(way)

    def __str__(self) -> str:
        str = ""
        for i in range(len(self.ftbsets)):
            for j in range(len(self.ftbsets[i].ftbways)):
                if self.ftbsets[i].ftbways[j].valid:
                    str += "\n"
                    str += f"[{i}][{j}]: "
                    str += f"{hex(self.ftbsets[i].ftbways[j].tag)} "
        return str

    