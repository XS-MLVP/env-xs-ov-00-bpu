import mlvp
import logging

import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from env.bpu_top import *

os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from env.bundle import *
from drivers.config import *
from drivers.utils import gen_update_request, generate_pc
from drivers.ftb_way import generate_new_ftb_entry

os.sys.path.append(FTB_DUT_PATH)

from UT_FTB import *

def set_imm_mode(FTB):
    imm_mode = FTB.io_s0_fire_0.xdata.Imme
    need_to_write_imm = ["io_s0_fire_0", "io_s0_fire_1", "io_s0_fire_2", "io_s0_fire_3",
                        "io_s1_fire_0", "io_s2_fire_0", "io_in_bits_s0_pc_0", "io_in_bits_s0_pc_1",
                        "io_in_bits_s0_pc_2", "io_in_bits_s0_pc_3", "reset"]
    for name in need_to_write_imm:
        getattr(FTB, name).xdata.SetWriteMode(imm_mode)

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
    g2.add_watch_point(FTB.io_out_s2_full_pred_3_hit, { "hit": fc.Eq(1), "not_hit": fc.Eq(0) }, name="s2_full_pred_0_hit")
    g2.add_watch_point(FTB.io_out_s3_full_pred_3_fallThroughErr, { "fallThroughErr_true": fc.Eq(1), "fallThroughErr_false": fc.Eq(0) }, name="s2_full_pred_3_fallThroughErr")
    g2.add_watch_point(FTB.io_out_s3_full_pred_3_slot_valids_0, { "slot_valids_0": fc.Eq(1), "slot_valids_0_invalid": fc.Eq(0) }, name="s2_full_pred_3_slot_valids_0")
    g2.add_watch_point(FTB.io_out_s3_full_pred_3_slot_valids_1, { "slot_valids_1": fc.Eq(1), "slot_valids_1_invalid": fc.Eq(0) }, name="s2_full_pred_3_slot_valids_1")
    g2.add_watch_point(FTB.io_out_s3_full_pred_3_br_taken_mask_0, { "br_taken_mask_0": fc.Eq(1), "br_taken_mask_0_invalid": fc.Eq(0) }, name="s2_full_pred_3_br_taken_mask_0")
    g2.add_watch_point(FTB.io_out_s3_full_pred_3_br_taken_mask_1, { "br_taken_mask_1": fc.Eq(1), "br_taken_mask_1_invalid": fc.Eq(0) }, name="s2_full_pred_3_br_taken_mask_1")
    g2.add_watch_point(FTB.io_out_s3_full_pred_3_is_br_sharing, { "is_br_sharing": fc.Eq(1), "is_br_sharing_invalid": fc.Eq(0) }, name="s2_full_pred_3_is_br_sharing")

    g3 = fc.CovGroup("ftb_slot")
    g3.add_watch_point(FTB.io_update_bits_ftb_entry_brSlots_0_tarStat, { "hit_2": fc.Eq(2), "hit_1": fc.Eq(1), "hit_0": fc.Eq(0) }, name="brSlots_0_tarStat_hit")
    g3.add_watch_point(FTB.io_update_bits_ftb_entry_tailSlot_tarStat, { "hit_2": fc.Eq(2), "hit_1": fc.Eq(1), "hit_0": fc.Eq(0) }, name="tailSlot_tarStat_hit")

    FTB.xclock.StepRis(lambda _: g1.sample())
    FTB.xclock.StepRis(lambda _: g2.sample())
    FTB.xclock.StepRis(lambda _: g3.sample())

    # Run the test
    mlvp.setup_logging(log_level=logging.INFO, log_file="report/ftb_bank.log")
    mlvp.run(run(FTB))
    FTB.finalize()

    pred_stat.summary()
    set_func_coverage(request, [g1, g2, g3])
    set_line_coverage(request, "report/ftb_bank_coverage.dat")


async def run(FTB):

    FTB_update = UpdateBundle.from_prefix("io_update_").set_name("FTB_update").bind(FTB)
    FTB_out = BranchPredictionResp.from_prefix("io_out_").set_name("FTB_out").bind(FTB)
    pipeline_ctrl = PipelineCtrlBundle.from_prefix("io_").set_name("pipeline_ctrl").bind(FTB)
    enable_ctrl = EnableCtrlBundle.from_prefix("io_ctrl_").set_name("enable_ctrl").bind(FTB)
    io_in = IoInBundle.from_prefix("io_in_").set_name("io_in").bind(FTB)

    bpu = BPUTop(FTB, FTB_out, FTB_update, pipeline_ctrl, enable_ctrl, io_in)

    mlvp.create_task(mlvp.start_clock(FTB))

    await control_signal_test_1(bpu)
    await control_signal_test_2(bpu)
    await control_signal_test_3(bpu)
    await ctest(bpu)
    # await control_signal_test_4(bpu)
    # await control_signal_test_5(bpu)


    # await ClockCycles(FTB, MAX_CYCLE)

async def control_signal_test_1(bpu):
    await bpu.reset()

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_1 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay=0)) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))
    case_part_3 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3


    for i in range(len(cases)):
        if i == radix * 2:
            await bpu.reset()

        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        if i < radix:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 2)
        elif i >= radix and i < radix + 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= radix + 1 and i < radix * 2:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
        else:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0

    info("[控制信号测试1] reset test [pass]")

async def control_signal_test_2(bpu):
    await bpu.reset()

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_1 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay=0),
                          1) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None, 1) for i in range(radix)))
    case_part_3 = tuple(((generate_pc(0x1, 0x1 * i), None, 0) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3


    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1,
                                         btb_enable = cases[i][2])
        
        if i < radix:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= radix and i < radix + 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= radix + 1 and i < radix * 2:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
        else:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0

    info("[控制信号测试2] io_ctrl_btb_enable test [pass]")

async def control_signal_test_3(bpu):
    await bpu.reset()

    radix = 1
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_1 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay=0),
                          1, 1, 1) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 0, 0) for i in range(radix)))
    case_part_3 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 0, 1) for i in range(radix)))
    case_part_4 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 1, 0) for i in range(radix)))
    case_part_5 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 1, 1) for i in range(radix)))
    case_part_6 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 1) for i in range(radix)))
    case_part_7 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 0, 0) for i in range(radix)))
    case_part_8 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 0, 1) for i in range(radix)))
    case_part_9 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 0) for i in range(radix)))
    case_part_10 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 1) for i in range(radix)))
    case_part_11 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 1, 1) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3 + \
            case_part_4 + case_part_5 + case_part_6 + \
            case_part_7 + case_part_8 + case_part_9 + \
            case_part_10 + case_part_11


    for i in range(len(cases)):
        
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = cases[i][2],
                                         s1_fire = cases[i][3],
                                         s2_fire = cases[i][4],)
        
        if i < 1:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 2)
        elif i >= 1 and i < 5:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= 5 and i < 6:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
        elif i >= 6 and i < 7:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 1
        elif i >= 7 and i < 8:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= 8 and i < 9:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        else:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1

    info("[控制信号测试3] io_s0_fire_0 test [pass]")

async def control_signal_test_4(bpu):
    await bpu.reset()

    radix = 1
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_0 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay=0),
                          1, 1, 1) for i in range(radix))
    case_part_1 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 0, 0) for i in range(radix)))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 0, 1) for i in range(radix)))
    case_part_3 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 0) for i in range(radix)))
    case_part_4 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 1) for i in range(radix)))
    case_part_5 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 1, 1) for i in range(radix)))
    case_part_6 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 0, 0) for i in range(radix)))
    case_part_7 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 0, 0) for i in range(radix)))

    cases = case_part_0 + case_part_1 + case_part_2 + case_part_3 + \
            case_part_4 + case_part_5 + case_part_6 + case_part_7
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = cases[i][2],
                                         s1_fire = cases[i][3],
                                         s2_fire = cases[i][4],)
        
        if i < 1:
            # await ClockCycles(bpu.dut, 2)
            # assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
            # assert bpu.dut.io_out_s3_full_pred_0_hit.value == 0
            await ClockCycles(bpu.dut, 2)
        elif i >= 1 and i < 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_hit.value == 0
        elif i >= 3 and i < 4:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_hit.value == 0
        else:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_hit.value == 1

    info("[控制信号测试4] io_s(1、2)_fire_0 test [pass]")

async def ctest(bpu):
    await bpu.reset()

    radix = 1
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_0 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay=0),
                          1, 1, 1) for i in range(radix))

    cases = case_part_0
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = cases[i][2],
                                         s1_fire = cases[i][3],
                                         s2_fire = cases[i][4],)

    await ClockCycles(bpu.dut, 10)

    info("[控制信号测试4] io_s(1、2)_fire_0 test [pass]")

async def control_signal_test_5(bpu):
    await bpu.reset()

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_0 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1 * i, 0x1), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay=0),
                          1, 0, 0) for i in range(radix))
    case_part_1 = tuple(((generate_pc(0x1 * i, 0x1), None, 1, 1, 0) for i in range(radix)))
    case_part_2 = tuple(((generate_pc(0x1 * i, 0x1), None, 1, 0, 1) for i in range(radix))) 
    case_part_3 = tuple(((generate_pc(0x1 * i, 0x1), None, 1, 1, 1) for i in range(radix))) 

    cases = case_part_0 + case_part_1 + case_part_2 + case_part_3
            
    for i in range(len(cases)):

        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = cases[i][2],
                                         s1_fire = cases[i][3],
                                         s2_fire = cases[i][4],)
        
        if i < 8:
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == 0
            assert meta['hit'] == 1
            await ClockCycles(bpu.dut, 2)
        elif i >= 8 and i < 12:
            await ClockCycles(bpu.dut, 2)
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == 3
            assert meta['hit'] == 1
        elif i == 12:
            await ClockCycles(bpu.dut, 2)
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == 0
            assert meta['hit'] == 1
        elif i == 13:
            await ClockCycles(bpu.dut, 2)
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == 1
            assert meta['hit'] == 1
        elif i == 14:
            await ClockCycles(bpu.dut, 2)
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == 2
            assert meta['hit'] == 1
        elif i == 15:
            await ClockCycles(bpu.dut, 2)
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == 3
            assert meta['hit'] == 1


    info("[控制信号测试5] last_stage_meta test [pass]")