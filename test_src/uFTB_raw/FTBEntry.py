from types import SimpleNamespace
import random


class FTBEntry:

    
    class BrSlot:
        valid=False
        offset=0
        target=0
        targetCoA=0
        alwaysTaken=False

    class TailSlot:
        valid=False
        offset=0
        target=0
        targetCoA=0
        alwaysTaken=False
        is_br_sharing=False

    def __init__(self):
        self.valid = False
        self.brSlot = self.BrSlot()
        self.tailSlot = self.TailSlot()
        
        self.pftAddr = 0
        self.carry = False
        self.isCall = False
        self.isRet = False
        self.isJalr = False
        self.rviCall = False

        self.brSlot.valid = False
        self.tailSlot.valid = False


def gen_ftb_entry(pc, br_slotv, tail_slotv) -> FTBEntry:
    entry = FTBEntry()
    entry.valid = True
    if br_slotv:
        entry.brSlot.valid = True
        entry.brSlot.target = random.randint(0, 2**20)
        entry.brSlot.offset = random.randint(0, 2**12)
        entry.brSlot.alwaysTaken = random.choice([True, False])
    if tail_slotv:
        entry.tailSlot.valid = True
        entry.tailSlot.target = random.randint(0, 2**20)
        entry.tailSlot.offset = random.randint(0, 2**12)
        entry.tailSlot.is_br_sharing = random.choice([True, False])
    entry.pftAddr = pc + random.randint(0, 2**12)
    if tail_slotv and entry.tailSlot.is_br_sharing == False:
        flag = random.randint(0, 3)
        if flag == 0:
            entry.isCall = True
        elif flag == 1:
            entry.isRet = True
        elif flag == 2:
            entry.isJalr = True
        else:
            entry.rviCall = True
    return entry
