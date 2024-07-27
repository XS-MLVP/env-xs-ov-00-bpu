import mlvp
import logging

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from env.bundle import *
from env.bpu_top import *
from env.config import *

os.sys.path.append(DUT_PATH)

from UT_FTB import *

def set_imm_mode(FTB):
    imm_mode = FTB.io_s0_fire_0.xdata.Imme
    need_to_write_imm = ["io_s0_fire_0", "io_s0_fire_1", "io_s0_fire_2", "io_s0_fire_3",
                        "io_s1_fire_0", "io_s2_fire_0", "io_in_bits_s0_pc_0", "io_in_bits_s0_pc_1",
                        "io_in_bits_s0_pc_2", "io_in_bits_s0_pc_3"]
    for name in need_to_write_imm:
        getattr(FTB, name).xdata.SetWriteMode(imm_mode)


async def ftb_test(FTB):
    FTB_update = UpdateBundle.from_prefix("io_update_").set_name("FTB_update").bind(FTB)
    FTB_out = BranchPredictionResp.from_prefix("io_out_").set_name("FTB_out").bind(FTB)
    pipeline_ctrl = PipelineCtrlBundle.from_prefix("io_").set_name("pipeline_ctrl").bind(FTB)
    enable_ctrl = EnableCtrlBundle.from_prefix("io_ctrl_").set_name("enable_ctrl").bind(FTB)
    io_in = IoInBundle.from_prefix("io_in_").set_name("io_in").bind(FTB)

    mlvp.create_task(mlvp.start_clock(FTB))
    mlvp.create_task(BPUTop(FTB, FTB_out, FTB_update, pipeline_ctrl, enable_ctrl, io_in).run())

    await ClockCycles(FTB, MAX_CYCLE)



import mlvp.funcov as fc
from mlvp.reporter import *

def test_ftb(request):
    # Create DUT
    FTB = DUTFTB(waveform_filename="report/ftb_bank.fst", coverage_filename="report/ftb_bank_coverage.dat")
    FTB.init_clock("clock")
    print(FTB.clock)
    set_imm_mode(FTB)

    # Set Coverage
    g1 = fc.CovGroup("interaction")
    g1.add_watch_point(FTB.reset, { "reset": fc.Eq(1), }, name="reset")
    g1.add_watch_point(FTB.io_ctrl_btb_enable, { "btb_enable": fc.Eq(1), }, name="btb_enable")
    g1.add_watch_point(FTB.io_s0_fire_0, { "s0_fire": fc.Eq(1), }, name="s0_fire_0")
    g1.add_watch_point(FTB.io_s1_fire_0, { "s1_fire": fc.Eq(1), }, name="s1_fire_0")
    g1.add_watch_point(FTB.io_s2_fire_0, { "s2_fire": fc.Eq(1), }, name="s2_fire_0")
    g1.add_watch_point(FTB.io_update_valid, { "update_valid": fc.Eq(1), }, name="update_valid")

    g2 = fc.CovGroup("ftb_entry")
    g2.add_watch_point(FTB.io_out_s2_full_pred_0_hit, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="s1_full_pred_0_hit")
    g2.add_watch_point(FTB.io_out_s2_full_pred_3_fallThroughErr, { "fallThroughErr": fc.Eq(1), "not_fallThroughErr": fc.Eq(0) }, name="s1_full_pred_3_fallThroughErr")
    g2.add_watch_point(FTB.io_out_s2_full_pred_0_slot_valids_0, { "slot_valids_0": fc.Eq(1), "slot_valids_0_invalid": fc.Eq(0) }, name="s1_full_pred_0_slot_valids_0")
    g2.add_watch_point(FTB.io_out_s2_full_pred_0_slot_valids_1, { "slot_valids_1": fc.Eq(1), "slot_valids_1_invalid": fc.Eq(0) }, name="s1_full_pred_0_slot_valids_1")
    g2.add_watch_point(FTB.io_out_s2_full_pred_0_br_taken_mask_0, { "br_taken_mask_0": fc.Eq(1), "br_taken_mask_0_invalid": fc.Eq(0) }, name="s1_full_pred_0_br_taken_mask_0")
    g2.add_watch_point(FTB.io_out_s2_full_pred_0_br_taken_mask_1, { "br_taken_mask_1": fc.Eq(1), "br_taken_mask_1_invalid": fc.Eq(0) }, name="s1_full_pred_0_br_taken_mask_1")
    g2.add_watch_point(FTB.io_out_s2_full_pred_0_is_br_sharing, { "is_br_sharing": fc.Eq(1), "is_br_sharing_invalid": fc.Eq(0) }, name="s1_full_pred_0_is_br_sharing")

    g3 = fc.CovGroup("ftb_slot")
    g3.add_watch_point(FTB.io_update_bits_ftb_entry_brSlots_0_tarStat, { "hit_2": fc.Eq(2), "hit_1": fc.Eq(1), "hit_0": fc.Eq(0) }, name="brSlots_0_tarStat_hit")
    g3.add_watch_point(FTB.io_update_bits_ftb_entry_tailSlot_tarStat, { "hit_2": fc.Eq(2), "hit_1": fc.Eq(1), "hit_0": fc.Eq(0) }, name="tailSlot_tarStat_hit")

    FTB.xclock.StepRis(lambda _: g1.sample())
    FTB.xclock.StepRis(lambda _: g2.sample())
    FTB.xclock.StepRis(lambda _: g3.sample())

    # Run the test
    mlvp.setup_logging(log_level=logging.DEBUG, log_file="report/ftb_bank.log")
    mlvp.run(ftb_test(FTB))
    FTB.finalize()

    pred_stat.summary()
    set_func_coverage(request, [g1, g2, g3])
    set_line_coverage(request, "report/ftb_bank_coverage.dat")
