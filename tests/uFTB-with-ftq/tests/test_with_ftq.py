import mlvp

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from env.bundle import *
from env.bpu_top import *
from env.config import *

os.sys.path.append(DUT_PATH)

from UT_FauFTB import *
uFTB = DUTFauFTB()
uFTB.init_clock("clock")

def set_imm_mode():
    imm_mode = uFTB.io_s0_fire_0.xdata.Imme
    need_to_write_imm = ["io_s0_fire_0", "io_s0_fire_1", "io_s0_fire_2", "io_s0_fire_3",
                        "io_s1_fire_0", "io_s2_fire_0", "io_in_bits_s0_pc_0", "io_in_bits_s0_pc_1",
                        "io_in_bits_s0_pc_2", "io_in_bits_s0_pc_3"]
    for name in need_to_write_imm:
        getattr(uFTB, name).xdata.SetWriteMode(imm_mode)

set_imm_mode()

async def uftb_test():
    uFTB_update = UpdateBundle.from_prefix(uFTB, "io_update_")
    uFTB_out = BranchPredictionResp.from_prefix(uFTB, "io_out_")
    pipeline_ctrl = PipelineCtrlBundle.from_prefix(uFTB, "io_")
    enable_ctrl = EnableCtrlBundle.from_prefix(uFTB, "io_ctrl_")

    mlvp.create_task(mlvp.start_clock(uFTB))
    mlvp.create_task(BPUTop(uFTB, uFTB_out, uFTB_update, pipeline_ctrl, enable_ctrl).run())

    await ClockCycles(uFTB, MAX_CYCLE)



import mlvp.funcov as fc
from mlvp.reporter import *

def test_uftb(request):
    g = fc.CovGroup("coverage_group_1")
    g.add_watch_point(uFTB.io_s0_fire_0, {
        "s0_fire": fc.Eq(1),
    }, name="s0_fire_0")

    set_func_coverage(request, g)
    set_line_coverage(request, "VFauFTB_coverage.dat")

    mlvp.run(uftb_test())
    g.sample()

    uFTB.finalize()
    pred_stat.summary()
