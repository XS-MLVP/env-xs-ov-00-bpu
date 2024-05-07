from typing import List, Tuple
from FauFTB import *
from FTBEntry import *

EntryList: List[Tuple[int, FTBEntry, bool, bool]] = []


def ftb_entry_list():
    for i in range(10000):
        pc = random.randint(0, 2**39)
        gentry = gen_ftb_entry(pc, True, True)
        EntryList.append(
            (pc, gentry, random.choice([True, False]), random.choice([True, False]))
        )
        # print("ftb_entry_list", EntryList[i][1].brSlot)
    return EntryList


def get_pred(uFTB: FauFTB, pc: int) -> Tuple[int, FTBEntry, bool, bool]:
    uFTB.io_in_bits_s0_pc.set(pc)
    uFTB.io_ctrl_ubtb_enable.value = 1
    uFTB.io_s0_fire.set(1)
    uFTB.io_s1_fire_0.value = 1
    uFTB.io_s2_fire_0.value = 1
    return uFTB.s1_full_pred()


def set_update(uFTB: FauFTB, entry: Tuple[int, FTBEntry, bool, bool]):
    uFTB.io_update_valid.value = True
    uFTB.io_update_bits_pc.value = entry[0]
    # print("set_update", entry[1].brSlot)
    uFTB.update_ftb_entry(entry[0], entry[1], (entry[2], entry[3]))


import mlvp.funcov as fc
from mlvp.reporter import *


def test_raw(request):

    uFTB: FauFTB = FauFTB(
        waveform_filename="report/uftb_raw.fst", coverage_filename="report/uftb_raw_coverage.dat"
    )
    ftb_entry_list()
    uFTB.reset.value = 1
    uFTB.Step(100)
    uFTB.reset.value = 0

    for i in range(10000):
        # print("main1", EntryList[i - 10][1].brSlot)
        j = i
        pred = get_pred(uFTB, EntryList[j][0])
        if i > 9:
            # print("main2", EntryList[i - 10][1].brSlot)
            set_update(uFTB, EntryList[(i - 10)%10000]) # update data 10 cycles ago
            pass
        print("main", pred[0], pred[1].__dict__)
        uFTB.Step(1)

    uFTB.finalize()

    set_line_coverage(request, "report/uftb_raw_coverage.dat")


if __name__ == "__main__":
    test_raw()
