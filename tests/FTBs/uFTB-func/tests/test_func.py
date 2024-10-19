import mlvp
import logging

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from drivers.utils import gen_update_request
from drivers.ftb_way import generate_new_ftb_entry
from drivers.config import *

from env.bpu_top import *
from env.bundle import *

os.sys.path.append(uFTB_DUT_PATH)

from UT_FauFTB import *

def set_imm_mode(uFTB, i: bool = False):
    imm_mode = uFTB.io_s0_fire_0.xdata.Imme
    need_to_write_imm = ["io_s0_fire_0", "io_s0_fire_1", "io_s0_fire_2", "io_s0_fire_3",
                        "io_s1_fire_0", "io_s2_fire_0", "io_in_bits_s0_pc_0", 
                        "io_in_bits_s0_pc_1", "io_in_bits_s0_pc_2", "io_in_bits_s0_pc_3", 
                        "reset"]
    if i:
        need_to_write_imm.remove("reset")

    for name in need_to_write_imm:
        getattr(uFTB, name).xdata.SetWriteMode(imm_mode)

import mlvp.funcov as fc
from mlvp.reporter import *

def test_uftb_func(request):
    # Create DUT

    uFTB = DUTFauFTB(waveform_filename="report/uftb_func.fst", 
                     coverage_filename="report/uftb_func_coverage.dat")
    uFTB.init_clock("clock")
    print(uFTB.clock)
    set_imm_mode(uFTB)

    g1 = fc.CovGroup("control signal")
    g2 = fc.CovGroup("update control")

    g1.add_watch_point(uFTB.reset, { "reset": fc.Eq(1), }, name="reset")
    g1.add_watch_point(uFTB.io_ctrl_ubtb_enable, { "ubtb_enable": fc.Eq(1), }, name="ubtb_enable")
    g1.add_watch_point(uFTB.io_s0_fire_0, { "s0_fire": fc.Eq(1), }, name="s0_fire_0")
    g1.add_watch_point(uFTB.io_s1_fire_0, { "s1_fire": fc.Eq(1), }, name="s1_fire_0")
    g1.add_watch_point(uFTB.io_s2_fire_0, { "s2_fire": fc.Eq(1), }, name="s2_fire_0")

    g2.add_watch_point(uFTB.io_update_valid, { "update_valid": fc.Eq(1), "update_not_valid": fc.Eq(0) }, name="update_valid")
    g2.add_watch_point(uFTB.io_update_bits_br_taken_mask_0, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="update_bits_br_taken_mask_0")
    g2.add_watch_point(uFTB.io_update_bits_br_taken_mask_1, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="update_bits_br_taken_mask_1")
    g2.add_watch_point(uFTB.io_update_bits_ftb_entry_always_taken_0, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="update_bits_ftb_entry_always_taken_0")
    g2.add_watch_point(uFTB.io_update_bits_ftb_entry_always_taken_1, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="update_bits_ftb_entry_always_taken_1")
    g2.add_watch_point(uFTB.io_update_bits_ftb_entry_tailSlot_sharing, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="update_bits_ftb_entry_tailSlot_sharing")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_0_hit, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="s1_full_pred_0_hit")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_3_fallThroughErr, { "fallThroughErr": fc.Eq(1), "not_fallThroughErr": fc.Eq(0) }, name="s1_full_pred_3_fallThroughErr")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_0_slot_valids_0, { "slot_valids_0": fc.Eq(1), "slot_valids_0_invalid": fc.Eq(0) }, name="s1_full_pred_0_slot_valids_0")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_0_slot_valids_1, { "slot_valids_1": fc.Eq(1), "slot_valids_1_invalid": fc.Eq(0) }, name="s1_full_pred_0_slot_valids_1")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_0_br_taken_mask_0, { "br_taken_mask_0": fc.Eq(1), "br_taken_mask_0_invalid": fc.Eq(0) }, name="s1_full_pred_0_br_taken_mask_0")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_0_br_taken_mask_1, { "br_taken_mask_1": fc.Eq(1), "br_taken_mask_1_invalid": fc.Eq(0) }, name="s1_full_pred_0_br_taken_mask_1")
    g2.add_watch_point(uFTB.io_out_s1_full_pred_0_is_br_sharing, { "is_br_sharing": fc.Eq(1), "is_br_sharing_invalid": fc.Eq(0) }, name="s1_full_pred_0_is_br_sharing")

    uFTB.xclock.StepRis(lambda _: g1.sample())
    uFTB.xclock.StepRis(lambda _: g2.sample())

    mlvp.setup_logging(log_level=logging.INFO, log_file="report/uftb_func.log")

    mlvp.run(run(uFTB))
    uFTB.finalize()

    pred_stat.summary()
    set_func_coverage(request, [g1, g2])
    set_line_coverage(request, "report/uftb_func_coverage.dat")

async def run(uFTB):

    uFTB_update = UpdateBundle.from_prefix("io_update_").set_name("uFTB_update").bind(uFTB)
    uFTB_out = BranchPredictionResp.from_prefix("io_out_").set_name("uFTB_out").bind(uFTB)
    pipeline_ctrl = PipelineCtrlBundle.from_prefix("io_").set_name("pipeline_ctrl").bind(uFTB)
    enable_ctrl = EnableCtrlBundle.from_prefix("io_ctrl_").set_name("enable_ctrl").bind(uFTB)

    bpu = BPUTop(uFTB, uFTB_out, uFTB_update, pipeline_ctrl, enable_ctrl)


    mlvp.create_task(mlvp.start_clock(uFTB))
    await control_signal_test_1(bpu)
    await control_signal_test_2(bpu)
    await control_signal_test_3(bpu)
    await control_signal_test_4(bpu)
    await br_taken_mask_test_1(bpu)
    await br_taken_mask_test_2(bpu)
    await br_taken_mask_test_3(bpu)
    await br_taken_mask_test_4(bpu)
    await br_taken_mask_test_5(bpu)
    await br_taken_mask_test_6(bpu)
    await br_taken_mask_test_7(bpu)
    await br_taken_mask_test_8(bpu)
    await br_taken_mask_test_9(bpu)
    await br_taken_mask_test_10(bpu)
    await br_taken_mask_test_11(bpu)
    await always_taken_test_1(bpu)
    await always_taken_test_2(bpu)
    await always_taken_test_3(bpu)
    await update_control_test_1(bpu)
    await ftb_update_test_1(bpu)
    await ftb_update_test_2(bpu)
    await ftb_update_test_3(bpu)
    await ftb_update_test_4(bpu)
    await ftb_update_test_5(bpu)
    await line_cov(bpu)

    # await ClockCycles(uFTB, MAX_CYCLE)


async def control_signal_test_1(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry() for _ in range(10)))

    case_part_1 = tuple(((0x1000, gen_update_request(0x10 * i, entrys[i], (1, 1))) for i in range(10)))
    case_part_2 = tuple(((0x10 * i, None) for i in range(10)))
    case_part_3 = tuple(((0x10 * i, None) for i in range(10)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        if i == 20:
            await bpu.reset()

        output, _ = await bpu.drive_once(cases[i][0], 
                                         cases[i][1])

        if i < 10:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 10 and i < 20:
            assert output["s1"]["full_pred"]["hit"] == 1
        else:
            assert output["s1"]["full_pred"]["hit"] == 0

    info("[控制信号测试1] reset test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)
    
async def control_signal_test_2(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry() for _ in range(10)))

    case_part_1 = tuple(((0x1000, # pc 
              gen_update_request(0x10 * i, entrys[i], (1, 1)), # update_request
              None, # redirect_request
              1 # ubtb_enable
              ) for i in range(10)))
    case_part_2 = tuple(((0x10 * i, None, None, 1) for i in range(10)))
    case_part_3 = tuple(((0x10 * i, None, None, 0) for i in range(10)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], 
                                      cases[i][1], 
                                      cases[i][2], 
                                      ubtb_enable = cases[i][3])

        if i < 10:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 10 and i < 21:
            assert output["s1"]["full_pred"]["hit"] == 1
        else:
            assert output["s1"]["full_pred"]["hit"] == 0


    info("[控制信号测试2] io_ctrl_ubtb_enable test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def control_signal_test_3(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry() for _ in range(10)))
         
    case_part_1 = tuple(((0x1000, # pc 
              gen_update_request(0x10 * i, entrys[i], (1, 1)), # update_request
              None, # redirect_request
              1 # io_s0_fire_0
              ) for i in range(10)))
    case_part_2 = tuple(((0x10 * i, None, None, 1) for i in range(10)))
    case_part_3 = tuple(((0x10 * i, None, None, 0) for i in range(10)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], 
                                      cases[i][1], 
                                      cases[i][2], 
                                      s0_fire = cases[i][3])

        if i < 10:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 10 and i < 20:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["pc_0"] == cases[i][0]
            assert output["s1"]["pc_1"] == cases[i][0]
            assert output["s1"]["pc_2"] == cases[i][0]
            assert output["s1"]["pc_3"] == cases[i][0]
            temp = output
        else:
            assert output == temp


    info("[控制信号测试3] io_s0_fire_0 test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def control_signal_test_4(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry() for _ in range(10)))

    case_part_1 = tuple(((0x1000, # pc 
              gen_update_request(0x10 * i, entrys[i], (1, 1)), # update_request
              None, # redirect_request
              1, # io_s0_fire_0
              1, # io_s1_fire_0
              1 # io_s2_fire_0
              ) for i in range(10)))
    case_part_2 = tuple(((0x10 * i, None, None, 1, 0, 0) for i in range(10)))
    case_part_3 = tuple(((0x10 * i, None, None, 1, 0, 1) for i in range(10)))
    case_part_4 = tuple(((0x10 * i, None, None, 1, 1, 0) for i in range(10)))
    case_part_5 = tuple(((0x10 * i, None, None, 1, 1, 1) for i in range(10)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5

    for i in range(len(cases)):
        # info(i)
        output, module_output = await bpu.drive_once(cases[i][0], 
                                      cases[i][1], 
                                      cases[i][2], 
                                      s0_fire = cases[i][3],
                                      s1_fire = cases[i][4],
                                      s2_fire = cases[i][5])

        if i < 10:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 10 and i < 20:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["last_stage_meta"] == 0
        elif i >= 20 and i < 30:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["last_stage_meta"] == 0
        elif i >= 30 and i < 40:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["last_stage_meta"] == 0
        else:
            meta = parse_uftb_meta(output["last_stage_meta"])
            assert meta["pred_way"] == (0 if module_output is None else module_output[2])
            assert meta["hit"] == 1


    info("[控制信号测试4] io_s1_fire_0 and io_s2_fire_0 test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_1(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[饱和计数器测试1] br_slot counter update (2-3-3) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_2(bpu):
    await bpu.reset()
    
    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[饱和计数器测试2] br_slot counter update (2-3-2) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_3(bpu):
    await bpu.reset()
    
    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 32 and i < 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
        elif i >= 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1

    info("[饱和计数器测试3] br_slot counter update (2-1-2) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_4(bpu):
    await bpu.reset()
    
    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 32 and i < 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
        elif i >= 64 and i < 96:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
        elif i >= 96:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[饱和计数器测试4] br_slot counter update (2-1-0-1) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_5(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_5 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[饱和计数器测试5] br_slot counter update (2-1-0-0) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_6(bpu):
    await bpu.reset()
    
    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_5 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_4 + case_part_5

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 32 and i < 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
        elif i >= 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1

    info("[饱和计数器测试6] tail_slot counter update (2-3-3) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_7(bpu):
    await bpu.reset()
    
    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[饱和计数器测试7] tail_slot counter update (2-3-2) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_8(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 32 and i < 62:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1

    info("[饱和计数器测试8] tail_slot counter update (2-1-2) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_9(bpu):
    await bpu.reset()
    
    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 1))) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 32 and i < 64:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 64 and i < 96:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 96:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0


    info("[饱和计数器测试9] tail_slot counter update (2-1-0-1) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_10(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0))) 
                          for i in range(32)))
    case_part_5 = tuple(((0x10 * i, # 0
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0


    info("[饱和计数器测试10] tail_slot counter update (2-1-0-0) test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def br_taken_mask_test_11(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry(is_sharing = 1) for _ in range(32)))

    case_part_1 = tuple(((0x10000, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, # 1
                          gen_update_request(0x10 * i, entrys[i], (1, 1)))  
                          for i in range(32)))
    case_part_3 = tuple(((0x10 * i, # 1
                          gen_update_request(0x10 * i, entrys[i], (0, 0)))  
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0)))  
                          for i in range(32)))
    case_part_5 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0)))  
                          for i in range(32)))
    case_part_6 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (0, 0)))  
                          for i in range(32)))
    case_part_7 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_8 = tuple(((0x10 * i, # 0
                          gen_update_request(0x10 * i, entrys[i], (1, 1)))  
                          for i in range(32)))
    case_part_9 = tuple(((0x10 * i, # 1
                          None)  
                          for i in range(32)))
    

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5 + case_part_6 + case_part_7 + case_part_8 + case_part_9

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 32 and i < 96:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
        elif i >= 96 and i < 128:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 128 and i < 256:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        elif i >= 256 and i < 288:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0


    info("[饱和计数器测试11] counter general update test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def always_taken_test_1(bpu):
    await bpu.reset()

    entry = generate_new_ftb_entry(is_sharing = 1,
                                   is_0_taken = 1)

    #         pc          update_request
    cases = ((0x0,        gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, None),)

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 3:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0


    info("[always_taken测试1] io_update_bits_ftb_entry_always_taken_0 test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def always_taken_test_2(bpu):
    await bpu.reset()

    entry = generate_new_ftb_entry(is_sharing = 1,
                                   is_1_taken = 1)

    #         pc          update_request
    cases = ((0x0,        gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, None),)

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 3:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[always_taken测试2] io_update_bits_ftb_entry_always_taken_1 test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def always_taken_test_3(bpu):
    await bpu.reset()

    entry = generate_new_ftb_entry(is_sharing = 0)

    #         pc          update_request
    cases = ((0x0,        gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, gen_update_request(0x80000010, entry, (0, 0))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, None),)

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 3:
            assert output["s1"]["full_pred"]["hit"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 0
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1


    info("[always_taken测试3] tailSlot_sharing test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def update_control_test_1(bpu):
    await bpu.reset()

    entry_before = tuple((generate_new_ftb_entry(is_sharing=1) for _ in range(32)))
    entry_after = tuple((generate_new_ftb_entry(is_sharing=0) for _ in range(32)))

    case_part_1 = tuple(((0x1000, 
                          gen_update_request(0x10 * i, entry_before[i], (1, 1), valid = True)) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, 
                          None) 
                          for i in range(32)))
    case_part_3 = tuple(((0x1000, 
                          gen_update_request(0x10 * i, entry_after[i], (1, 1), valid = False)) 
                          for i in range(32)))
    case_part_4 = tuple(((0x10 * i, 
                          None) 
                          for i in range(32)))
    case_part_5 = tuple(((0x1000, 
                          gen_update_request(0x10 * i, entry_after[i], (1, 1), valid = True)) 
                          for i in range(32)))
    case_part_6 = tuple(((0x10 * i, 
                          None) 
                          for i in range(32)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5 + case_part_6 

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if (i < 32) or (i >= 64 and i < 96) or (i >= 128 and i < 160):
            assert output["s1"]["full_pred"]["hit"] == 0
        elif (i >= 32 and i < 64) or (i >= 96 and i < 128):
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["slot_valids_0"] == 1
            assert output["s1"]["full_pred"]["slot_valids_1"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
            assert output["s1"]["full_pred"]["is_br_sharing"] == 1
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["slot_valids_0"] == 1
            assert output["s1"]["full_pred"]["slot_valids_1"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
            assert output["s1"]["full_pred"]["is_br_sharing"] == 0


    info("[更新控制信号测试1] io_update_valid test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def ftb_update_test_1(bpu):
    await bpu.reset()

    entry = generate_new_ftb_entry(is_sharing = 0)

    #         pc          update_request
    cases = ((0x0,        gen_update_request(0x80000010, entry, (1, 1))),
             (0x80000010, None),
             (0x80000010, None),
             (0x80000010, None),)

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 3:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 3 and i < 9:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["slot_valids_0"] == 1
            assert output["s1"]["full_pred"]["slot_valids_1"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
            assert output["s1"]["full_pred"]["is_br_sharing"] == 0


    info("[FTB项更新1] FTB_way update test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)
    
async def ftb_update_test_2(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry() for _ in range(32)))

    case_part_1 = tuple(((0x1000, 
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, None) for i in range(32)))

    cases = case_part_1 + case_part_2

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["slot_valids_0"] == 1
            assert output["s1"]["full_pred"]["slot_valids_1"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1
            assert output["s1"]["full_pred"]["is_br_sharing"] == 1


    info("[FTB项更新2] update hit test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def ftb_update_test_3(bpu):
    await bpu.reset()
    
    entrys_1 = tuple((generate_new_ftb_entry() for _ in range(32)))
    entrys_2 = tuple((generate_new_ftb_entry() for _ in range(16)))

    case_part_1 = tuple(((0x10000, 
                          gen_update_request(0x10 * i, entrys_1[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10000, 
                          gen_update_request(0x10 * i, entrys_1[i], (1, 1))) 
                          for i in range(16)))
    case_part_3 = tuple(((0x10000, 
                          gen_update_request(0x700 + 0x10 * i, entrys_2[i], (1, 1))) 
                          for i in range(16)))
    case_part_4 = tuple(((0x10 * i, None) for i in range(16, 32)))
    case_part_5 = tuple(((0x700 + 0x10 * i, None) for i in range(16)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 32 and i < 48:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 48 and i < 64:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 64 and i < 80:
            assert output["s1"]["full_pred"]["hit"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1


    info("[FTB项更新3] update not hit, LRU update test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def ftb_update_test_4(bpu):
    await bpu.reset()
    
    entrys_1 = tuple((generate_new_ftb_entry() for _ in range(32)))
    entrys_2 = tuple((generate_new_ftb_entry() for _ in range(16)))

    case_part_1 = tuple(((0x10000, 
                          gen_update_request(0x10 * i, entrys_1[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, 
                          None) 
                          for i in range(16)))
    case_part_3 = tuple(((0x10000, 
                          gen_update_request(0x700 + 0x10 * i, entrys_2[i], (1, 1))) 
                          for i in range(16)))
    case_part_4 = tuple(((0x10 * i, None) for i in range(16, 32)))
    case_part_5 = tuple(((0x700 + 0x10 * i, None) for i in range(16)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 32 and i < 48:
            assert output["s1"]["full_pred"]["hit"] == 1
        elif i >= 48 and i < 64:
            assert output["s1"]["full_pred"]["hit"] == 0
        elif i >= 64 and i < 80:
            assert output["s1"]["full_pred"]["hit"] == 1
        else:
            assert output["s1"]["full_pred"]["hit"] == 1


    info("[FTB项更新4] update not hit, LRU not update test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def ftb_update_test_5(bpu):
    await bpu.reset()

    entrys = tuple((generate_new_ftb_entry(is_sharing=0) for _ in range(32)))

    case_part_1 = tuple(((0x1000, 
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(32)))
    case_part_2 = tuple(((0x10 * i, None) for i in range(32)))

    cases = case_part_1 + case_part_2

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 32:
            assert output["s1"]["full_pred"]["hit"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["slot_valids_0"] == 1
            assert output["s1"]["full_pred"]["slot_valids_1"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1

    info("[FTB项更新5] update not sharing way test [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

async def line_cov(bpu):
    await bpu.reset()

    entrys_1 = tuple((generate_new_ftb_entry(is_sharing=0, 
                                           br_0_start_pc = 1 << 12, 
                                           br_0_target_addr = 2 << 12) for _ in range(1)))
    
    entrys_2 = tuple((generate_new_ftb_entry(is_sharing=0, 
                                           br_0_start_pc = 2 << 12, 
                                           br_0_target_addr = 1 << 12) for _ in range(1)))
    
    entrys_3 = tuple((generate_new_ftb_entry(is_sharing=0, 
                                           br_0_start_pc = 1 << 12, 
                                           br_0_target_addr = 1 << 12) for _ in range(1)))
    
    entrys = entrys_1 + entrys_2 + entrys_3

    case_part_1 = tuple(((0x1000, 
                          gen_update_request(0x10 * i, entrys[i], (1, 1))) 
                          for i in range(3)))
    case_part_2 = tuple(((0x10 * i, None) for i in range(3)))

    cases = case_part_1 + case_part_2

    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

        if i < 3:
            assert output["s1"]["full_pred"]["hit"] == 0
        else:
            assert output["s1"]["full_pred"]["hit"] == 1
            assert output["s1"]["full_pred"]["slot_valids_0"] == 1
            assert output["s1"]["full_pred"]["slot_valids_1"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_0"] == 1
            assert output["s1"]["full_pred"]["br_taken_mask_1"] == 1

    info("[FTB项更新5] io_update_bits_ftb_entry_brSlots_0_tarStat coverage [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

