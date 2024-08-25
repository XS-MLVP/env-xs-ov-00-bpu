import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from mlvp import *
from drivers.bundle import *
from drivers.ftq import *
from .uftb_model import uFTBModel

def assert_equal(a, b, key: str = ""):
    if a != b:
        error(f"[Error] Expected is {a}, but actual is {b}. " + key)
        exit(1)

def compare_uftb_full_pred(uftb_output, std_output):
    need_compare = ["hit", "slot_valids_0", "slot_valids_1", "targets_0", "targets_1",
                    "offsets_0", "offsets_1", "fallThroughAddr", "is_br_sharing",
                    "br_taken_mask_0", "br_taken_mask_1"]
    for key in need_compare:
        assert_equal(uftb_output[key], std_output[key], key)

class BPUTop:
    def __init__(self, dut, dut_out: BranchPredictionResp, dut_update: UpdateBundle, pipeline_ctrl: PipelineCtrlBundle, enable_ctrl: EnableCtrlBundle):
        self.dut = dut

        self.dut_out = dut_out
        self.dut_update = dut_update
        self.pipeline_ctrl = pipeline_ctrl
        self.enable_ctrl = enable_ctrl

        self.s0_fire = 0
        self.s1_fire = 0
        self.s2_fire = 0
        self.s3_fire = 0
        self.s0_pc = RESET_VECTOR
        self.s1_pc = 0
        self.s2_pc = 0
        self.s3_pc = 0
        self.s1_hit_way = 0
        self.s2_hit_way = 0
        self.s3_hit_way = 0

        self.npc_gen = 0
        self.next_s0_fire = 0
        self.s1_flush = False
        self.s2_flush = False
        self.s3_flush = False

        self.ftq = FTQ()
        self.uftb_model = uFTBModel()
        self.ftb_provider = FTBProvider()

    def pipeline_assign(self, s0_f, s1_f, s2_f, s0_pc, ubtb_enable):
        self.pipeline_ctrl.s0_fire_0.value = s0_f
        self.pipeline_ctrl.s0_fire_1.value = s0_f
        self.pipeline_ctrl.s0_fire_2.value = s0_f
        self.pipeline_ctrl.s0_fire_3.value = s0_f
        assert_equal(self.pipeline_ctrl.s0_fire_0.value, s0_f)
        assert_equal(self.pipeline_ctrl.s0_fire_1.value, s0_f)
        assert_equal(self.pipeline_ctrl.s0_fire_2.value, s0_f)
        assert_equal(self.pipeline_ctrl.s0_fire_3.value, s0_f)

        self.pipeline_ctrl.s1_fire_0.value = s1_f
        assert_equal(self.pipeline_ctrl.s1_fire_0.value, s1_f)

        self.pipeline_ctrl.s2_fire_0.value = s2_f
        assert_equal(self.pipeline_ctrl.s2_fire_0.value, s2_f)

        # Set the value to 1 forcibly to obtain meta information
        self.dut.io_s1_fire_0.value = s1_f
        self.dut.io_s2_fire_0.value = s2_f

        self.dut.io_in_bits_s0_pc_0.value = s0_pc
        self.dut.io_in_bits_s0_pc_1.value = s0_pc
        self.dut.io_in_bits_s0_pc_2.value = s0_pc
        self.dut.io_in_bits_s0_pc_3.value = s0_pc

        assert_equal(self.dut.io_in_bits_s0_pc_0.value, s0_pc)
        assert_equal(self.dut.io_in_bits_s0_pc_1.value, s0_pc)
        assert_equal(self.dut.io_in_bits_s0_pc_2.value, s0_pc)
        assert_equal(self.dut.io_in_bits_s0_pc_3.value, s0_pc)

        self.enable_ctrl.ubtb_enable.value = ubtb_enable
        assert_equal(self.dut.io_ctrl_ubtb_enable.value, ubtb_enable) 

    async def io_set(self):
        self.dut_out.last_stage_meta.value = 0
        self.dut.io_out_last_stage_meta.value = 0
        # self.dut_out.s1.pc_0.value = 0
        # self.dut_out.s1.pc_1.value = 0
        # self.dut_out.s1.pc_2.value = 0
        # self.dut_out.s1.pc_3.value = 0
        # self.dut_out.s1.valid.value = 1
        # self.dut_out.s1.hasRedirect.value = 0
        # self.dut_out.s1.ftq_idx.value = 0
        # self.dut_out.s1.full_pred.hit.value = 0
        # self.dut_out.s1.full_pred.slot_valids_0.value = 0
        # self.dut_out.s1.full_pred.slot_valids_1.value = 0
        # self.dut_out.s1.full_pred.targets_0.value = 0
        # self.dut_out.s1.full_pred.targets_1.value = 0
        # self.dut_out.s1.full_pred.offsets_0.value = 0
        # self.dut_out.s1.full_pred.offsets_1.value = 0
        # self.dut_out.s1.full_pred.fallThroughAddr.value = 0
        # self.dut_out.s1.full_pred.fallThroughErr.value = 0
        # self.dut_out.s1.full_pred.is_jal.value = 0
        # self.dut_out.s1.full_pred.is_jalr.value = 0
        # self.dut_out.s1.full_pred.is_call.value = 0
        # self.dut_out.s1.full_pred.is_ret.value = 0
        # self.dut_out.s1.full_pred.is_br_sharing.value = 0
        # self.dut_out.s1.full_pred.last_may_be_rvi_call.value = 0
        # self.dut_out.s1.full_pred.br_taken_mask_0.value = 0
        # self.dut_out.s1.full_pred.br_taken_mask_1.value = 0
        # self.dut_out.s1.full_pred.jalr_target.value = 0

    def generate_bpu_output(self, dut_output):
        dut_output["s1"]["valid"] = self.s1_fire
        dut_output["s2"]["valid"] = self.s2_fire
        dut_output["s3"]["valid"] = self.s3_fire

        dut_output["s2"]["pc_1"] = self.s2_pc
        dut_output["s2"]["pc_2"] = self.s2_pc
        dut_output["s2"]["pc_3"] = self.s2_pc
        dut_output["s3"]["pc_1"] = self.s3_pc
        dut_output["s3"]["pc_2"] = self.s3_pc
        dut_output["s3"]["pc_3"] = self.s3_pc

        # Provide Basic FTB Prediction
        ftb_provider_stage_enable = (False, False, False)

        if self.s1_fire and ftb_provider_stage_enable[0]:
            ftb_entry = self.ftb_provider.provide_ftb_entry(self.s1_fire, self.s1_pc)
            if ftb_entry is not None:
                ftb_entry.put_to_full_pred_dict(self.s1_pc, dut_output["s1"]["full_pred"])
            else:
                set_all_none_item_to_zero(dut_output["s1"]["full_pred"])

        if self.s2_fire and ftb_provider_stage_enable[1]:
            ftb_entry = self.ftb_provider.provide_ftb_entry(self.s2_fire, self.s2_pc)
            if ftb_entry is not None:
                ftb_entry.put_to_full_pred_dict(self.s2_pc, dut_output["s2"]["full_pred"])
            else:
                set_all_none_item_to_zero(dut_output["s2"]["full_pred"])

        if self.s3_fire and ftb_provider_stage_enable[2]:
            ftb_entry = self.ftb_provider.provide_ftb_entry(self.s3_fire, self.s3_pc)
            if ftb_entry is not None:
                ftb_entry.put_to_full_pred_dict(self.s3_pc, dut_output["s3"]["full_pred"])
                dut_output["last_stage_ftb_entry"] = ftb_entry.__dict__()
            else:
                set_all_none_item_to_zero(dut_output["s3"]["full_pred"])
                dut_output["last_stage_ftb_entry"] = FTBEntry().__dict__()

        return dut_output

    async def run(self):
        self.uftb_model.ubtb_enable.value = 1
        self.s0_pc = RESET_VECTOR

        await self.reset()

        while True:
            self.pipeline_assign(self.s0_fire, self.s1_fire, self.s2_fire, self.s0_pc, 1)
            await ClockCycles(self.dut, 1)
            self.step_assign()
            bpu_output, model_output, std_ftb_entry = await self.one_step_stage_one()
            
            update_request, redirect_request = self.ftq.update(bpu_output, std_ftb_entry)

            await self.one_step_stage_two(update_request, redirect_request)

    def step_assign(self):
        self.s3_fire = self.s2_fire
        self.s2_fire = self.s1_fire
        self.s1_fire = self.s0_fire
        self.s3_pc = self.s2_pc
        self.s2_pc = self.s1_pc
        self.s1_pc = self.s0_pc
        self.s3_hit_way = self.s2_hit_way
        self.s2_hit_way = self.s1_hit_way

        self.npc_gen = self.s0_pc
        self.next_s0_fire = 1
        self.s1_flush = False
        self.s2_flush = False
        self.s3_flush = False

    async def reset(self):
        self.dut.reset.value = 1
        await ClockCycles(self.dut, 1)
        self.dut.reset.value = 0
        await ClockCycles(self.dut, 1)
        self.uftb_model = uFTBModel()

    async def drive_once(self, 
                         s0_pc, 
                         update_request: dict, 
                         redirect_request: dict = None, 
                         s0_fire: int = 1, 
                         s1_fire: int = 0, 
                         s2_fire: int = 0, 
                         ubtb_enable: int = 1):

        self.pipeline_assign(s0_fire, s1_fire, s2_fire, s0_pc, ubtb_enable)
        self.s0_pc = s0_pc
        self.s0_fire = s0_fire
        self.s1_fire = s1_fire
        self.s2_fire = s2_fire

        await ClockCycles(self.dut, 1)
        bpu_output, module_output, std_ftb_entry = await self.one_step_stage_one()
        # update_request, redirect_request = self.ftq.update(bpu_output, std_ftb_entry)
        await self.one_step_stage_two(update_request, redirect_request)

        self.uftb_model.ubtb_enable = ubtb_enable

        return bpu_output, module_output

    async def one_step_stage_one(self):
        # self.uftb_model.print_all_ftb_ways()

        # Get dut output and generate bpu output
        # await self.io_set()
        dut_output = self.dut_out.as_dict()
        bpu_output = self.generate_bpu_output(dut_output)

        ftb_entry = FTBEntry.from_full_pred_dict(self.s0_pc, dut_output["s1"]["full_pred"])
        model_output = self.uftb_model.generate_output(self.s0_fire, self.s0_pc)
        std_ftb_entry = self.ftb_provider.provide_ftb_entry(self.s0_fire, self.s0_pc)

        if model_output[0] is not None:
            meta_hit_way = model_output[2]
        else:
            meta_hit_way = None

        if self.s0_fire:
            # Compare dut output and uFTB model output
            expected_hit = model_output[0] is not None
            actual_hit = bpu_output["s1"]["full_pred"]["hit"]
            # info(model_output)
            # info(dut_output)
            assert_equal(expected_hit, actual_hit)
            if self.s1_fire and self.s2_fire:
                if parse_uftb_meta(dut_output["last_stage_meta"])["hit"] or meta_hit_way is not None:
                    actual_hit_way = parse_uftb_meta(dut_output["last_stage_meta"])["pred_way"]
                    assert_equal(meta_hit_way, actual_hit_way)

            if model_output[0]:
                std_full_pred = {}
                model_output[0].put_to_full_pred_dict(self.s0_pc, std_full_pred)
                std_full_pred["br_taken_mask_0"] = model_output[1][0]
                std_full_pred["br_taken_mask_1"] = model_output[1][1]
                compare_uftb_full_pred(std_full_pred, bpu_output["s1"]["full_pred"])

        # Forward to FTQ and get update and redirect request
        if self.s1_fire:
            self.npc_gen = get_target_from_full_pred_dict(self.s0_pc, dut_output["s1"]["full_pred"])

        return bpu_output, model_output, std_ftb_entry
        

    async def one_step_stage_two(self, update_request, redirect_request):
        ## Update Request
        if update_request:
            self.dut_update.valid.value = 1
            self.uftb_model.update(update_request)
            self.ftb_provider.update(update_request)
            self.dut_update.assign(update_request)
        else:
            self.dut_update.valid.value = 0

        self.uftb_model._process_update()

        ## Redirect Request
        if redirect_request:
            self.next_s0_fire = 1
            self.s1_flush = True
            self.s2_flush = True
            self.s3_flush = True
            self.npc_gen = redirect_request["cfiUpdate"]["target"]

        # Add new control information
        self.s0_fire = self.next_s0_fire
        self.s0_pc = self.npc_gen
        if self.s1_flush:
            self.s1_fire = 0
        if self.s2_flush:
            self.s2_fire = 0
        if self.s3_flush:
            self.s3_fire = 0

        return self.s0_pc