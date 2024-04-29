from .utils import *

class FTBSlot:
    def __init__(self):
        self.valid = 0
        self.offset = 0
        self.lower = 0
        self.tarStart = 0
        self.sharing = 0

    def __str__(self, pc, is_cond_branch):
        str = ""
        if not self.valid:
            str += "*\tInvalid FTBSlot\n"
            return str

        if is_cond_branch:
            str += f"*\t[Conditional Branch Inst] at PC {hex(get_slot_addr(pc, self.offset))}: Target: {hex(get_target_addr(pc, self.tarStart, self.lower, 12))}\n"
        else:
            str += f"*\t[Jump Inst] PC {hex(get_slot_addr(pc, self.offset))}: Target: {hex(get_target_addr(pc, self.tarStart, self.lower, 20))}\n"

        return str


class FTBEntry:
    def __init__(self):
        self.valid = 0
        self.brSlot = FTBSlot()
        self.tailSlot = FTBSlot()
        self.pftAddr = 0
        self.carry = 0
        self.isCall = False
        self.isRet = False
        self.isJal = False
        self.isJalr = False
        self.last_may_be_rvi_call = False
        self.always_taken = [0, 0]

    def add_cond_branch_inst(self, start_pc, inst_pc, is_taken, target_addr):
        if self.brSlot.valid and self.tailSlot.valid:
            return False

        slot = FTBSlot()
        slot.valid = True
        slot.offset = get_slot_offset(start_pc, inst_pc)
        slot.lower = get_lower_addr(target_addr, 12)
        slot.tarStart = get_target_stat(start_pc >> 12, target_addr >> 12)

        if self.brSlot.valid:
            self.tailSlot = slot
            self.tailSlot.sharing = True
            self.always_taken[1] = is_taken
        else:
            self.brSlot = slot
            self.always_taken[0] = is_taken

        return True

    def add_jmp_inst(self, start_pc, inst_pc, target_addr, inst_len, is_call, is_ret, is_jalr, is_jal):
        if self.tailSlot.valid:
            return False

        self.tailSlot.valid = True
        self.tailSlot.offset = get_slot_offset(start_pc, inst_pc)
        self.tailSlot.lower = get_lower_addr(target_addr, 20)
        self.tailSlot.tarStart = get_target_stat(start_pc >> 20, target_addr >> 20)
        self.tailSlot.sharing = False

        self.isCall = is_call
        self.isRet = is_ret
        self.isJalr = is_jalr
        self.isJal = is_jal
        self.last_may_be_rvi_call = is_call and inst_len == 4

        return True

    def put_to_full_pred_dict(self, pc, d):
        d["hit"] = 1
        d["slot_valids_0"] = self.brSlot.valid
        d["slot_valids_1"] = self.tailSlot.valid
        d["targets_0"] = get_target_addr(pc, self.brSlot.tarStart, self.brSlot.lower, 12)
        d["targets_1"] = get_target_addr(pc, self.tailSlot.tarStart, self.tailSlot.lower, 12 if self.tailSlot.sharing else 20)
        d["offsets_0"] = self.brSlot.offset
        d["offsets_1"] = self.tailSlot.offset
        d["fallThroughErr"] = get_fallthrough_addr(pc, self.pftAddr, self.carry) <= pc
        d["fallThroughAddr"] = get_fallthrough_addr(pc, self.pftAddr, self.carry) if not d["fallThroughErr"] else pc + (PREDICT_WIDTH_BYTES)
        d["is_jal"] = self.isJal
        d["is_jalr"] = self.isJalr
        d["is_call"] = self.isCall
        d["is_ret"] = self.isRet
        d["is_br_sharing"] = self.tailSlot.sharing
        d["last_may_be_rvi_call"] = self.last_may_be_rvi_call
        d["br_taken_mask_0"] = self.always_taken[0]
        d["br_taken_mask_1"] = self.always_taken[1]
        d["jalr_target"] = get_target_addr(pc, self.tailSlot.tarStart, self.tailSlot.lower, 20)


    def __dict__(self):
        return {
            "brSlots_0_offset": self.brSlot.offset,
            "brSlots_0_lower": self.brSlot.lower,
            "brSlots_0_tarStat": self.brSlot.tarStart,
            "brSlots_0_valid": self.brSlot.valid,
            "tailSlot_offset": self.tailSlot.offset,
            "tailSlot_lower": self.tailSlot.lower,
            "tailSlot_tarStat": self.tailSlot.tarStart,
            "tailSlot_sharing": self.tailSlot.sharing,
            "tailSlot_valid": self.tailSlot.valid,
            "pftAddr": self.pftAddr,
            "carry": self.carry,
            "isCall": self.isCall,
            "isRet": self.isRet,
            "isJalr": self.isJalr,
            "last_may_be_rvi_call": self.last_may_be_rvi_call,
            "always_taken_0": self.always_taken[0],
            "always_taken_1": self.always_taken[1]
        }

    @classmethod
    def from_dict(self, d):
        entry = FTBEntry()
        entry.brSlot.offset = d["brSlots_0_offset"]
        entry.brSlot.lower = d["brSlots_0_lower"]
        entry.brSlot.tarStart = d["brSlots_0_tarStat"]
        entry.brSlot.valid = d["brSlots_0_valid"]
        entry.tailSlot.offset = d["tailSlot_offset"]
        entry.tailSlot.lower = d["tailSlot_lower"]
        entry.tailSlot.tarStart = d["tailSlot_tarStat"]
        entry.tailSlot.sharing = d["tailSlot_sharing"]
        entry.tailSlot.valid = d["tailSlot_valid"]
        entry.pftAddr = d["pftAddr"]
        entry.carry = d["carry"]
        entry.isCall = d["isCall"]
        entry.isRet = d["isRet"]
        entry.isJalr = d["isJalr"]
        entry.last_may_be_rvi_call = d["last_may_be_rvi_call"]
        entry.always_taken[0] = d["always_taken_0"]
        entry.always_taken[1] = d["always_taken_1"]
        return entry

    @classmethod
    def from_full_pred_dict(self, pc, d):
        entry = FTBEntry()
        entry.brSlot.valid = d["slot_valids_0"]
        entry.brSlot.offset = d["offsets_0"]
        entry.brSlot.lower = get_lower_addr(d["targets_0"], 12)
        entry.brSlot.tarStart = get_target_stat(pc >> 12, d["targets_0"] >> 12)
        entry.tailSlot.valid = d["slot_valids_1"]
        entry.tailSlot.offset = d["offsets_1"]
        entry.tailSlot.sharing = d["is_br_sharing"]

        if entry.tailSlot.sharing:
            entry.tailSlot.lower = get_lower_addr(d["targets_1"], 12)
            entry.tailSlot.tarStart = get_target_stat(pc >> 12, d["targets_1"] >> 12)
        else:
            entry.tailSlot.lower = get_lower_addr(d["targets_1"], 20)
            entry.tailSlot.tarStart = get_target_stat(pc >> 20, d["targets_1"] >> 20)

        entry.pftAddr = get_pftaddr(d["fallThroughAddr"])
        entry.carry = get_pftaddr_carry(pc, d["fallThroughAddr"])
        entry.isCall = d["is_call"]
        entry.isRet = d["is_ret"]
        entry.isJal = d["is_jal"]
        entry.isJalr = d["is_jalr"]
        entry.last_may_be_rvi_call = d["last_may_be_rvi_call"]
        entry.always_taken[0] = d["br_taken_mask_0"]
        entry.always_taken[1] = d["br_taken_mask_1"]

        return entry

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

class FTBProvider():
    def __init__(self):
        self.entries = {}

    def update(self, update_request):
        if update_request["valid"]:
            self.entries[update_request["bits_pc"]] = FTBEntry.from_dict(update_request["ftb_entry"])

    def provide_ftb_entry(self, fire, pc):
        if fire and pc in self.entries:
            return self.entries[pc]
        else:
            return None
