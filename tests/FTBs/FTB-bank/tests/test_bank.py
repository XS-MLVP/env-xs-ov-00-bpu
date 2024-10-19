import mlvp
import logging
from mlvp.modules import PLRU

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
    # g3.add_watch_point(FTB.io_update_bits_ftb_entry_tailSlot_tarStat, { "hit_2": fc.Eq(2), "hit_1": fc.Eq(1), "hit_0": fc.Eq(0) }, name="tailSlot_tarStat_hit")

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
    # reset bug here
    await reset_bug(bpu) 
    await control_signal_test_4(bpu)
    await control_signal_test_5(bpu)
    await pred_way_out_1(bpu)
    await pred_way_out_2(bpu)
    await pred_way_out_3(bpu)
    await pred_way_out_4(bpu)
    await update_signal_test_1(bpu)
    await update_signal_test_2(bpu)
    await update_signal_test_3(bpu)
    await update_test_1(bpu)
    await update_test_2(bpu)
    await update_test_3(bpu)
    await update_test_4(bpu)
    await line_cov(bpu)

    

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
                                             meta_writeWay= 0 )) for i in range(radix))
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
                          gen_update_request(generate_pc(0x1 * i, 0x1), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 ),
                          1) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1 * i, 0x1), None, 1) for i in range(radix)))
    case_part_3 = tuple(((generate_pc(0x1 * i, 0x1), None, 0) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3


    for i in range(len(cases)):
        # info(i)
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
                                             meta_writeWay= 0 ),
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
    case_part_11 = tuple(((generate_pc(0x1, 0x1 * i), None, 0, 0, 0) for i in range(radix)))

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
        
        if i < 5:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
        elif i >= 5 and i < 6:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            await ClockCycles(bpu.dut, 1)
        else:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_hit.value == 1
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_hit.value == 1
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_hit.value == 1
            await ClockCycles(bpu.dut, 3)

    info("[控制信号测试3] s0_fire test [pass]")

async def reset_bug(bpu):
    await bpu.reset()

    radix = 1
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_0 = tuple((generate_pc(0x1, 0x0), 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 ),
                          1, 1, 1) for i in range(radix))

    cases = case_part_0
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = cases[i][2],
                                         s1_fire = cases[i][3],
                                         s2_fire = cases[i][4],)
        
        
        assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1 # 这里应该是0
        assert bpu.dut.io_out_s3_full_pred_0_hit.value == 0
        await ClockCycles(bpu.dut, 1)
        assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
        assert bpu.dut.io_out_s3_full_pred_0_hit.value == 1 # 这里应该是0
        await ClockCycles(bpu.dut, 1)
        assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
        assert bpu.dut.io_out_s3_full_pred_0_hit.value == 0
        await ClockCycles(bpu.dut, 1)

    await ClockCycles(bpu.dut, 10)

    info("[BUG HERE] reset bug")

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
                                             meta_writeWay= 0 ),
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

async def control_signal_test_5(bpu):
    await bpu.reset()

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_0 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 ),
                          1, 0, 0) for i in range(radix))
    case_part_1 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 0) for i in range(radix)))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 0, 1) for i in range(radix))) 
    case_part_3 = tuple(((generate_pc(0x1, 0x1 * i), None, 1, 1, 1) for i in range(radix))) 

    cases = case_part_0 + case_part_1 + case_part_2 + case_part_3 + case_part_3
            
    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = cases[i][2],
                                         s1_fire = cases[i][3],
                                         s2_fire = cases[i][4],)
        
        await ClockCycles(bpu.dut, 2)
        meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)

        if i < 8:
            assert meta['pred_way'] == 0
            assert meta['hit'] == 1
        elif i >= 8 and i < 12:
            assert meta['pred_way'] == 3
            assert meta['hit'] == 1
        elif i == 12:
            assert meta['pred_way'] == 0
            assert meta['hit'] == 1
        elif i == 13:
            assert meta['pred_way'] == 1
            assert meta['hit'] == 1
        elif i == 14:
            assert meta['pred_way'] == 2
            assert meta['hit'] == 1
        elif i == 15:
            assert meta['pred_way'] == 3
            assert meta['hit'] == 1
        elif i == 16:
            assert meta['pred_way'] == 0
            assert meta['hit'] == 1
        elif i == 17:
            assert meta['pred_way'] == 1
            assert meta['hit'] == 1
        elif i == 18:
            assert meta['pred_way'] == 2
            assert meta['hit'] == 1


    info("[控制信号测试5] last_stage_meta test [pass]")

async def pred_way_out_1(bpu):
    await bpu.reset()

    case_part_0 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x0), 
                                       generate_new_ftb_entry(is_0_taken=1, is_1_taken=0), 
                                       (1, 0), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_1 = (generate_pc(0x1, 0x0), None)
    case_part_2 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x1), 
                                       generate_new_ftb_entry(is_0_taken=0, is_1_taken=1), 
                                       (0, 1), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_3 = (generate_pc(0x1, 0x1), None)
    case_part_4 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x2), 
                                       generate_new_ftb_entry(is_0_taken=1, is_1_taken=1), 
                                       (1, 1), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_5 = (generate_pc(0x1, 0x2), None)

    cases = (case_part_0, case_part_1, \
            case_part_2, case_part_3, \
            case_part_4, case_part_5)
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                             update_request = cases[i][1],
                                             s0_fire = 1,
                                             s1_fire = 1,
                                             s2_fire = 1,
                                             s2_musk_0 = 0,
                                             s2_musk_1 = 0,
                                             s3_musk_0 = 0,
                                             s3_musk_1 = 0)
        
        if i == 0 or i == 2 or i == 4:
            await ClockCycles(bpu.dut, 2)
        elif i == 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
        elif i == 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1
        elif i == 5:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1

    info("[预测结果输出测试1] FTBBank hit, always_taken valid [pass]")

async def pred_way_out_2(bpu):
    await bpu.reset()

    case_part_0 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x0), 
                                       generate_new_ftb_entry(is_0_taken=0, is_1_taken=0), 
                                       (0, 0), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_1 = (generate_pc(0x1, 0x0), None)
    case_part_2 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x1), 
                                       generate_new_ftb_entry(is_0_taken=0, is_1_taken=0), 
                                       (0, 0), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_3 = (generate_pc(0x1, 0x1), None)


    cases = (case_part_0, case_part_1, \
            case_part_2, case_part_3)
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                             update_request = cases[i][1],
                                             s0_fire = 1,
                                             s1_fire = 1,
                                             s2_fire = 1,
                                             s2_musk_0 = 0 if i < 2 else 1,
                                             s2_musk_1 = 0 if i < 2 else 1,
                                             s3_musk_0 = 0 if i < 2 else 1,
                                             s3_musk_1 = 0 if i < 2 else 1)
        
        if i == 0 or i == 2:
            await ClockCycles(bpu.dut, 2)
        elif i == 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
        elif i == 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1

    info("[预测结果输出测试2] FTBBank hit, always_taken not valid [pass]")

async def pred_way_out_3(bpu):
    await bpu.reset()

    case_part_0 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x0), 
                                       generate_new_ftb_entry(is_0_taken=1, is_1_taken=1), 
                                       (1, 1), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_1 = (0x11000, None)
    case_part_2 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x1), 
                                       generate_new_ftb_entry(is_0_taken=1, is_1_taken=1), 
                                       (1, 1), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_3 = (0x11000, None)


    cases = (case_part_0, case_part_1, \
            case_part_2, case_part_3)
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                             update_request = cases[i][1],
                                             s0_fire = 1,
                                             s1_fire = 1,
                                             s2_fire = 1,
                                             s2_musk_0 = 0 if i < 2 else 1,
                                             s2_musk_1 = 0 if i < 2 else 1,
                                             s3_musk_0 = 0 if i < 2 else 1,
                                             s3_musk_1 = 0 if i < 2 else 1)
        
        if i == 0 or i == 2:
            await ClockCycles(bpu.dut, 2)
        elif i == 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
        elif i == 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1

    info("[预测结果输出测试3] FTBBank not hit, always_taken valid [pass]")

async def pred_way_out_4(bpu):
    await bpu.reset()

    case_part_0 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x0), 
                                       generate_new_ftb_entry(is_0_taken=0, is_1_taken=0), 
                                       (0, 0), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_1 = (0x11000, None)
    case_part_2 = (0x11000, 
                   gen_update_request(generate_pc(0x1, 0x1), 
                                       generate_new_ftb_entry(is_0_taken=0, is_1_taken=0), 
                                       (0, 0), 
                                       meta_hit = 0, 
                                       old_entry = 0,
                                       meta_writeWay= 0 ))
    case_part_3 = (0x11000, None)


    cases = (case_part_0, case_part_1, \
            case_part_2, case_part_3)
            
    for i in range(len(cases)):
        # info(i)
        output, model = await bpu.drive_once(cases[i][0], 
                                             update_request = cases[i][1],
                                             s0_fire = 1,
                                             s1_fire = 1,
                                             s2_fire = 1,
                                             s2_musk_0 = 0 if i < 2 else 1,
                                             s2_musk_1 = 0 if i < 2 else 1,
                                             s3_musk_0 = 0 if i < 2 else 1,
                                             s3_musk_1 = 0 if i < 2 else 1)
        
        if i == 0 or i == 2:
            await ClockCycles(bpu.dut, 2)
        elif i == 1:

            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 0
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 0
        elif i == 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s2_full_pred_0_br_taken_mask_1.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_0.value == 1
            assert bpu.dut.io_out_s3_full_pred_0_br_taken_mask_1.value == 1

    info("[预测结果输出测试4] FTBBank not hit, always_taken not valid [pass]")

async def update_signal_test_1(bpu):
    await bpu.reset(no_wait = True)

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_1 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))
    case_part_3 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_4 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4


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
        elif i >= radix and i < radix * 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= radix * 3 and i < radix * 3 + 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        else:
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1

    info("[更新控制信号测试1] s1_ready test [pass]")

async def update_signal_test_2(bpu):
    await bpu.reset()

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_1 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             valid = False,
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))
    case_part_3 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_4 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4


    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        if i < radix:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 2)
        elif i >= radix and i < radix * 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= radix * 3 and i < radix * 3 + 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        else:
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1

    info("[更新控制信号测试2] io_update_valid test [pass]")

async def update_signal_test_3(bpu):
    await bpu.reset()

    radix = 4
    entrys = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0) for _ in range(radix)))

    case_part_1 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 1,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))
    case_part_3 = tuple((0x10000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_4 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))

    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4


    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        if i < radix:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 2)
        elif i >= radix and i < radix * 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i >= radix * 3 and i < radix * 3 + 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        else:
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1

    info("[更新控制信号测试3] io_update_bits_old_entry test [pass]")

async def update_test_1(bpu):
    await bpu.reset()

    radix = 1
    entrys1 = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0, br_0_target_addr = 2) for _ in range(radix)))
    entrys2 = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0, br_0_target_addr = 4) for _ in range(radix)))
    entrys3 = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0, br_0_target_addr = 8) for _ in range(radix)))

    case_part_1 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys1[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_2 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))
    case_part_3 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys2[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_4 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))
    case_part_5 = tuple((0x11000, 
                          gen_update_request(generate_pc(0x1, 0x1 * i), 
                                             entrys3[i], 
                                             (1, 1), 
                                             meta_hit = 1, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) for i in range(radix))
    case_part_6 = tuple(((generate_pc(0x1, 0x1 * i), None) for i in range(radix)))


    cases = case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5 + case_part_6


    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        if i == 0 or i == 2 or i == 4:
            pass
        elif i == 1:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.targets_0.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.targets_0.value == 2
        elif i == 3:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.targets_0.value == 2
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.targets_0.value == 4
        elif i == 5:
            await ClockCycles(bpu.dut, 2)
            assert bpu.dut_out.s2.full_pred.targets_0.value == 8

    info("[FTB项更新测试1] meta hit test [pass]")

async def update_test_2(bpu):
    await bpu.reset()

    radix = 1
    entrys1 = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0, br_0_target_addr = 2, is_sharing=1 if random.randint(0, 1) == 1 else 0) for _ in range(2048)))

    case_part_1 = tuple(((0x11000, 
                          gen_update_request(generate_pc(0x1 * j, 0x1 * i), 
                                             entrys1[j * 4 + i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             for i in range(4) for j in range(512)))
    case_part_2 = tuple(((generate_pc(0x1 * j, 0x1 * i), None) 
                         for i in range(4) for j in range (512)))

    cases = case_part_1 + case_part_2

    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        if i < 2048:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
        elif i == 2048:
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 0
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 0
            await ClockCycles(bpu.dut, 1)
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == int(( i - 2048 ) / 512)
            assert meta['hit'] == 1
        else:
            assert bpu.dut_out.s2.full_pred.hit.value == 1
            assert bpu.dut_out.s3.full_pred.hit.value == 1
            await ClockCycles(bpu.dut, 2)
            meta = parse_uftb_meta(bpu.dut_out.last_stage_meta.value)
            assert meta['pred_way'] == int(( i - 2048 ) / 512)
            assert meta['hit'] == 1

    info("[FTB项更新测试2] target index calculation test [pass]")

async def update_test_3(bpu):
    await bpu.reset()

    entrys1 = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0, br_0_target_addr = 2) for _ in range(4)))

    case_part_0 = tuple(((0x110000, 
                          gen_update_request(generate_pc(0x1, 1 * i), 
                                             entrys1[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             for i in range(4)))
    case_part_1 = tuple(((generate_pc(0x1, 1 * i), None) for i in range(4)))
    case_part_2 = tuple(((0x110000, 
                          gen_update_request(generate_pc(0x1, 1 * i), 
                                             entrys1[i],  
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             for i in (0, 2)))
    case_part_3 = tuple(((0x110000, 
                          gen_update_request(generate_pc(0x1, 1 * i + 0x40), 
                                             entrys1[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             for i in range(2)))
    case_part_4 = tuple(((generate_pc(0x1, 1 * i), None) for i in range(4)))
    case_part_5 = tuple(((generate_pc(0x1, 1 * i + 0x40), None) for i in range(2)))
    case_part_6 = tuple(((0x110000, None) for i in range(2)))

    cases = case_part_0 + case_part_1 + case_part_2 + case_part_3 + case_part_4 + case_part_5 + case_part_6

    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        await bpu.drive_once(cases[i][0], 
                             None,
                             s0_fire = 1,
                             s1_fire = 1,
                             s2_fire = 1)
        
        await bpu.drive_once(cases[i][0], 
                             None,
                             s0_fire = 1,
                             s1_fire = 1,
                             s2_fire = 1)
        
        if i == 4:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 5:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 6:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 7:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 12:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 13:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
        elif i == 14:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 15:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
        elif i == 16:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 17:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1

    info("[FTB项更新测试3] update miss, LRU update test [pass]")

async def update_test_4(bpu):

    await bpu.reset()

    entrys1 = tuple((generate_new_ftb_entry(is_0_taken=0, is_1_taken=0, br_0_target_addr = 2) for _ in range(4)))

    case_part_0 = tuple(((0x110000, 
                          gen_update_request(generate_pc(0x1, 1 * i), 
                                             entrys1[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             for i in range(4)))
    case_part_1 = tuple(((generate_pc(0x1, 1 * i), None) for i in range(4)))
    case_part_3 = tuple(((0x110000, 
                          gen_update_request(generate_pc(0x1, 1 * i + 0x40), 
                                             entrys1[i], 
                                             (1, 1), 
                                             meta_hit = 0, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             for i in range(2)))
    case_part_4 = tuple(((generate_pc(0x1, 1 * i), None) for i in range(4)))
    case_part_5 = tuple(((generate_pc(0x1, 1 * i + 0x40), None) for i in range(2)))
    case_part_6 = tuple(((0x110000, None) for i in range(2)))

    cases = case_part_0 + case_part_1 + case_part_3 + case_part_4 + case_part_5 + case_part_6

    for i in range(len(cases)):
        output, model = await bpu.drive_once(cases[i][0], 
                                         update_request = cases[i][1],
                                         s0_fire = 1,
                                         s1_fire = 1,
                                         s2_fire = 1)
        
        await bpu.drive_once(cases[i][0], 
                             None,
                             s0_fire = 1,
                             s1_fire = 1,
                             s2_fire = 1)
        
        await bpu.drive_once(cases[i][0], 
                             None,
                             s0_fire = 1,
                             s1_fire = 1,
                             s2_fire = 1)
        
        if i == 4:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 5:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 6:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 7:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 10:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
        elif i == 11:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 12:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 0
        elif i == 13:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 14:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1
        elif i == 15:
            assert bpu.dut.io_out_s2_full_pred_0_hit.value == 1

    info("[FTB项更新测试4] update miss, LRU not update test [pass]")

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
    
    entrys_4 = tuple((generate_new_ftb_entry(is_sharing=0, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 2 << 12) for _ in range(1)))
    
    entrys_5 = tuple((generate_new_ftb_entry(is_sharing=0, 
                                           tail_start_pc = 2 << 12, 
                                           tail_target_addr = 1 << 12) for _ in range(1)))
    
    entrys_6 = tuple((generate_new_ftb_entry(is_sharing=0, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 1 << 12) for _ in range(1)))
    
    entrys_7 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 2 << 12) for _ in range(1)))
    
    entrys_8 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 2 << 12, 
                                           tail_target_addr = 1 << 12) for _ in range(1)))
    
    entrys_9 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 1 << 12) for _ in range(1)))

    entrys_10 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 2 << 12,
                                           valid=False) for _ in range(1)))
    
    entrys_11 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 2 << 12, 
                                           tail_target_addr = 1 << 12,
                                           valid=False) for _ in range(1)))
    
    entrys_12 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 1 << 12,
                                           valid=False) for _ in range(1)))
    
    entrys_13 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 1 << 12,
                                           last_may_be_rvi_call = 1) for _ in range(1)))
    
    entrys_14 = tuple((generate_new_ftb_entry(is_sharing=1, 
                                           tail_start_pc = 1 << 12, 
                                           tail_target_addr = 1 << 12,
                                           tail_slot_valid=False) for _ in range(1)))
    
    entrys = entrys_1 + entrys_2 + entrys_3 + entrys_4 + entrys_5 + entrys_6 + entrys_7 + entrys_8 + entrys_9 + entrys_10 + entrys_11 + entrys_12 + entrys_13 + entrys_14

    case_part_1 = tuple(((0x1000, 
                          gen_update_request(generate_pc(i, 0), 
                                             entrys[i], 
                                             (1, 1), 
                                             meta_hit = 1, 
                                             old_entry = 0,
                                             meta_writeWay= 0 )) 
                                             
                          for i in range(14)))
    case_part_2 = tuple(((generate_pc(i, 0), None) for i in range(14)))

    cases = case_part_1 + case_part_2


    for i in range(len(cases)):
        output, _ = await bpu.drive_once(cases[i][0], cases[i][1])

    info("[FTB项更新测试5] io_update_bits_ftb_entry_brSlots_0_tarStat coverage [pass]")
    # await ClockCycles(uFTB, MAX_CYCLE)

