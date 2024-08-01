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
        # self.update_hits = None
        self.update_access = None
        # self.update_write_alloc = None

        self.update_queue = []
        self.output_queue = []
        self.replacer_update_queue = [[], []]

    def find_set_from_idx(self, idx):
        for i in range(FTB_BANK_SETS_NUM):
            if self.ftbsets[i].idx == idx:
                return i
        return None
    
    def update(self, update_request):
        idx = FTBSet.get_idx(update_request["bits_pc"])
        tag = FTBWay.get_tag(update_request["bits_pc"])
        debug(f"Update request [{idx}] {hex(tag)}")
        # info(update_request)
        self.update_queue.append((update_request, 2, None, None))
    
    def generate_output(self, s0_fire, s1_fire, s2_fire, s3_fire, pc): 
        # debug(FTBSet.get_idx(s2_pc))
        debug(self)
        debug(f"{s0_fire}, {s1_fire}, {s2_fire}, {s3_fire}")
        debug(f"Generate output [{FTBSet.get_idx(pc)}] {hex(FTBWay.get_tag(pc))}")
        # self.process_update()
        if s0_fire:
            self.output_queue.append((pc, None, None, 2))

        s2 = (None, None)
        s3 = (None, None)

        new_output_queue = []
        
        for i in range(len(self.output_queue)):
            if self.output_queue[i][3] == 0: # s2_fire
                if s3_fire:
                    debug(f"Generate output [{FTBSet.get_idx(self.output_queue[i][0])}] {hex(FTBWay.get_tag(self.output_queue[i][0]))} stage 2")
                    s3 = (self.output_queue[i][1], self.output_queue[i][2])
            elif self.output_queue[i][3] == 1: # s1_fire
                read_resp, read_hits = self.process_read(self.output_queue[i][0])
                if s2_fire:
                    debug(f"Generate output [{FTBSet.get_idx(self.output_queue[i][0])}] {hex(FTBWay.get_tag(self.output_queue[i][0]))} stage 1")
                    new_output_queue.append((self.output_queue[i][0],
                                         read_resp,
                                         read_hits,
                                         self.output_queue[i][3] - 1))
                    s2 = (read_resp, read_hits)
            elif self.output_queue[i][3] == 2: # s0_fire
                debug(f"Generate output [{FTBSet.get_idx(self.output_queue[i][0])}] {hex(FTBWay.get_tag(self.output_queue[i][0]))} stage 0")
                new_output_queue.append((self.output_queue[i][0],
                                         self.output_queue[i][1],
                                         self.output_queue[i][2],
                                         self.output_queue[i][3] - 1))
                
        self.output_queue = new_output_queue
        
        # debug(f"generate_output output {s2} {s3}")

        return s2 + s3

    def process_read(self, req_pc):
        # lookup idx and tag
        idx = FTBSet.get_idx(req_pc)
        tag = FTBWay.get_tag(req_pc)

        # find FTBWay
        read_hits = self.ftbsets[idx].find_way_from_tag(tag)
        debug(f"Process_read read way {read_hits}")
        if read_hits is None:
            return None, None

        # return read_resp(the target FTBway) and read_hits(Which way is hit)
        read_resp = self.ftbsets[idx].ftbways[read_hits].ftb_entry

        self.replacer_update_queue[0].append((idx, read_hits, 2))
        # self._update_replacer(idx, read_hits)

        return read_resp, read_hits

    def process_update(self, s3_fire):
        for i in range(2):
            new_replacer_update_queue = []
            for j in range(len(self.replacer_update_queue[i])):
                if self.replacer_update_queue[i][j][2] == 0:
                    self._update_replacer(self.replacer_update_queue[i][j][0],
                                          self.replacer_update_queue[i][j][1])
                else:
                    new_replacer_update_queue.append((self.replacer_update_queue[i][j][0], 
                                             self.replacer_update_queue[i][j][1],
                                             self.replacer_update_queue[i][j][2] - 1))
            self.replacer_update_queue[i] = new_replacer_update_queue

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
                if meta["hit"] and s3_fire:
                    self._update_ways(FTBSet.get_idx(update_request["bits_pc"]), 
                                      meta["pred_way"], 
                                      update_request["bits_pc"], 
                                      update_request["ftb_entry"])
                    self.update_access = False
                else:
                    update_hits = self._update_read(update_request["bits_pc"])
                    new_update_queue.append((update_request, 
                                             clock_cycle - 1, 
                                             update_hits,
                                             update_write_alloc))
                    self.update_access = True
                
        self.update_queue = new_update_queue
        
    def _update_read(self, u_req_pc):
        idx = FTBSet.get_idx(u_req_pc)
        tag = FTBWay.get_tag(u_req_pc)

        way_index = self.ftbsets[idx].find_way_from_tag(tag)
        if way_index is not None:
            # hit
            return way_index
        else:
            # miss
            return None
        
    def _update_write(self, update_request, update_write_way, update_write_alloc: bool):
        pc = FTBWay.get_tag(update_request["bits_pc"])
        # debug(f"Write request {hex(pc)}")
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
                debug(f"Swap out [{idx}] [{replace_way}]")
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
        self.replacer_update_queue[1].insert(0, (idx,
                                                 way, 
                                                 0))
        debug(f"{hex(FTBWay.get_tag(pc))} is put to [{idx}] [{way}]")

    def _update_replacer(self, idx, way):
        debug(f"Update replacer [{idx}] [{way}]")
        self.ftbsets[idx].replacer.update(way)

    def __str__(self) -> str:
        str = ""
        start = 451
        for i in range(start, start + 1):
            for j in range(len(self.ftbsets[i].ftbways)):
                if self.ftbsets[i].ftbways[j].valid:
                    str += "\n"
                    str += f"[{i}][{j}]: "
                    str += f"{hex(self.ftbsets[i].ftbways[j].tag)} "
        return str

    