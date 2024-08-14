from mlvp import *
from .bundle import *
from .ftq import *
from .ftb_bank import FTBBank

def assert_equal(a, b):
    if a != b:
        error(f"[Error] UDT is {a}, but model is {b}")
        exit(1)

def compare_uftb_full_pred(ftb_output, std_output):

    need_compare = ["hit", "slot_valids_0", "slot_valids_1", "targets_0", "targets_1",
                    "offsets_0", "offsets_1", "fallThroughAddr", "is_br_sharing",
                    "br_taken_mask_0", "br_taken_mask_1"]
    # info("ftb_output:")
    # info(ftb_output)
    # info("std_output:")
    # info(std_output)
    for key in need_compare:
        assert_equal(ftb_output[key], std_output[key])



class BPUTop:
    def __init__(self, dut, dut_out: BranchPredictionResp, dut_update: UpdateBundle, pipeline_ctrl: PipelineCtrlBundle, enable_ctrl: EnableCtrlBundle, io_in: IoInBundle):
        self.dut = dut

        self.dut_out = dut_out
        self.dut_update = dut_update
        self.pipeline_ctrl = pipeline_ctrl
        self.enable_ctrl = enable_ctrl
        self.io_in = io_in

        self.s0_fire = 0
        self.s1_fire = 0
        self.s2_fire = 0
        self.s3_fire = 0
        self.s0_pc = 0
        self.s1_pc = 0
        self.s2_pc = 0
        self.s3_pc = 0
        self.s1_hit_way = 0
        self.s2_hit_way = 0
        self.s3_hit_way = 0

        self.ftq = FTQ()
        self.ftb_model = FTBBank()
        self.ftb_provider = FTBProvider()

    def pipeline_assign(self, s0_f, s1_f, s2_f, s0_pc, btb_enable):
        self.pipeline_ctrl.s0_fire_0.value = s0_f
        self.pipeline_ctrl.s0_fire_1.value = s0_f
        self.pipeline_ctrl.s0_fire_2.value = s0_f
        self.pipeline_ctrl.s0_fire_3.value = s0_f

        self.pipeline_ctrl.s1_fire_0.value = s1_f
        self.pipeline_ctrl.s1_fire_1.value = s1_f
        self.pipeline_ctrl.s1_fire_2.value = s1_f
        self.pipeline_ctrl.s1_fire_3.value = s1_f

        self.pipeline_ctrl.s2_fire_0.value = s2_f
        self.pipeline_ctrl.s2_fire_1.value = s2_f
        self.pipeline_ctrl.s2_fire_2.value = s2_f
        self.pipeline_ctrl.s2_fire_3.value = s2_f

        assert_equal(self.dut.io_s0_fire_0.value, s0_f)
        assert_equal(self.dut.io_s0_fire_1.value, s0_f)
        assert_equal(self.dut.io_s0_fire_2.value, s0_f)
        assert_equal(self.dut.io_s0_fire_3.value, s0_f)

        assert_equal(self.dut.io_s1_fire_0.value, s1_f)
        assert_equal(self.dut.io_s1_fire_1.value, s1_f)
        assert_equal(self.dut.io_s1_fire_2.value, s1_f)
        assert_equal(self.dut.io_s1_fire_3.value, s1_f)

        assert_equal(self.dut.io_s2_fire_0.value, s2_f)
        assert_equal(self.dut.io_s2_fire_1.value, s2_f)
        assert_equal(self.dut.io_s2_fire_2.value, s2_f)
        assert_equal(self.dut.io_s2_fire_3.value, s2_f)

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

        self.enable_ctrl.btb_enable.value = btb_enable
        assert_equal(self.dut.io_ctrl_btb_enable.value, btb_enable) 

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
        ftb_provider_stage_enable = (False, self.s2_fire, self.s3_fire)

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

    async def reset(self):
        self.dut.reset.value = 1
        await ClockCycles(self.dut, 1)
        self.dut.reset.value = 0
        await ClockCycles(self.dut, 1)
        self.ftb_model = FTBBank()

    def step_assign(self):
        self.s3_fire = self.s2_fire
        self.s2_fire = self.s1_fire
        self.s1_fire = self.s0_fire
        self.s3_pc = self.s2_pc
        self.s2_pc = self.s1_pc
        self.s1_pc = self.s0_pc
        self.s3_hit_way = self.s2_hit_way
        self.s2_hit_way = self.s1_hit_way
        
        debug(f"{self.s0_fire} {self.s1_fire} {self.s2_fire} {self.s3_fire}")

        self.npc_gen = self.s0_pc
        self.next_s0_fire = 1
        self.s1_flush = False
        self.s2_flush = False
        self.s3_flush = False

    def one_step_stage_one(self):
        self.ftb_model.process_update(self.s3_fire)

        # Get dut output and generate bpu output
        dut_output = self.dut_out.as_dict()
        # debug(dut_output)
        bpu_output = self.generate_bpu_output(dut_output)

        ftb_entry = FTBEntry.from_full_pred_dict(self.s0_pc, dut_output["s2"]["full_pred"])
        (s2_read_resp, s2_read_hits, s3_read_resp, s3_read_hits) = self.ftb_model.generate_output(self.s0_fire, 
                        self.s1_fire,
                        self.s2_fire, 
                        self.s3_fire, 
                        self.s0_pc)
        std_ftb_entry = self.ftb_provider.provide_ftb_entry(self.s2_fire, self.s0_pc)

        # Compare dut output and uFTB model output
        dut_s2_hit = bool(bpu_output["s2"]["full_pred"]["hit"])
        dut_s3_hit = bool(bpu_output["s3"]["full_pred"]["hit"])
        # info(bpu_output["s2"]["full_pred"]["hit"])
        model_s2_hit = s2_read_hits is not None
        model_s3_hit = s3_read_hits is not None
        assert_equal(dut_s2_hit, model_s2_hit)
        assert_equal(dut_s3_hit, model_s3_hit)


        if model_s2_hit or dut_s2_hit:
            model_s2_full_pred = {}
            s2_read_resp.put_to_full_pred_dict(self.s1_pc, model_s2_full_pred)
            compare_uftb_full_pred(bpu_output["s2"]["full_pred"], model_s2_full_pred)

        if model_s3_hit or dut_s3_hit:
            model_s3_full_pred = {}
            s3_read_resp.put_to_full_pred_dict(self.s2_pc, model_s3_full_pred)
            compare_uftb_full_pred(bpu_output["s3"]["full_pred"], model_s3_full_pred)

        if self.s3_fire:
            # debug(bin(self.dut.io_out_last_stage_meta.value))
            if parse_uftb_meta(dut_output["last_stage_meta"])["hit"] or self.s2_hit_way is not None:
                hit = parse_uftb_meta(dut_output["last_stage_meta"])["hit"]
                actual_hit_way = parse_uftb_meta(dut_output["last_stage_meta"])["pred_way"]
                debug(f"Dut_output last_stage_meta hit {hit} pred_way {actual_hit_way}")
                expected_hit_way = 0 if self.s2_hit_way is None else self.s2_hit_way
                assert_equal(actual_hit_way, expected_hit_way)

        # Forward to FTQ and get update and redirect request
        if self.s3_fire:
            npc_gen = get_target_from_full_pred_dict(self.s3_pc, dut_output["s3"]["full_pred"])
        

        return bpu_output, (s2_read_resp, s2_read_hits, s3_read_resp, s3_read_hits), std_ftb_entry

    def one_stage_step_two(self, update_request, redirect_request):
        ## Update Request
        if update_request:
            self.ftb_model.update(update_request)
            self.ftb_provider.update(update_request)
            # if update_request["bits_meta"] is None:
            #     update_request["bits_meta"] = 0
            del update_request['bits_br_taken_mask_0']
            del update_request['bits_br_taken_mask_1']
            self.dut_update.assign(update_request)
            self.dut_update.valid.value = 1
        else:
            self.dut_update.valid.value = 0

        ## Redirect Request
        if redirect_request:
            self.next_s0_fire = 1
            self.s1_flush = True
            self.s2_flush = True
            self.s3_flush = True
            self.npc_gen = redirect_request["cfiUpdate"]["target"]

        # Add new control information
        self.s0_fire = self.next_s0_fire
        self.s0_pc =self.npc_gen
        if self.s1_flush:
            self.s1_fire = 0
        if self.s2_flush:
            self.s2_fire = 0
        if self.s3_flush:
            self.s3_fire = 0

    async def run(self):
        self.enable_ctrl.btb_enable.value = 1
        self.s0_pc = RESET_VECTOR
        self.dut.io_reset_vector.value = RESET_VECTOR

        await self.reset()
        
        while True:
            self.pipeline_assign(self.s0_fire, self.s1_fire, self.s2_fire, self.s0_pc, 1)
            await ClockCycles(self.dut, 1)
            self.step_assign()
            debug("========tick========")

            bpu_output, model_output, std_ftb_entry = self.one_step_stage_one()

            update_request, redirect_request = self.ftq.update(bpu_output, std_ftb_entry)

            self.one_stage_step_two(update_request, redirect_request)

    async def drive_once(self, 
                         s0_pc, 
                         update_request: dict, 
                         redirect_request: dict = None, 
                         s0_fire: int = 1, 
                         s1_fire: int = 0, 
                         s2_fire: int = 0, 
                         btb_enable: int = 1):

        self.pipeline_assign(s0_fire, s1_fire, s2_fire, s0_pc, btb_enable)
        self.s0_pc = s0_pc
        self.s0_fire = s0_fire
        self.s1_fire = s1_fire
        self.s2_fire = s2_fire

        await ClockCycles(self.dut, 1)
        bpu_output, module_output, std_ftb_entry = await self.one_step_stage_one()
        # update_request, redirect_request = self.ftq.update(bpu_output, std_ftb_entry)
        await self.one_step_stage_two(update_request, redirect_request)

        self.ftb_model.btb_enable = btb_enable

        return bpu_output, module_output