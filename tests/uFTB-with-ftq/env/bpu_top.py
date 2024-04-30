from mlvp import *
from .bundle import *
from .ftq import *
from .uftb_model import uFTBModel

def assert_equal(a, b):
    if a != b:
        error(f"[Error] Expected is {a}, but actual is {b}")
        exit(1)

def compare_uftb_full_pred(uftb_output, std_output):
    need_compare = ["hit", "slot_valids_0", "slot_valids_1", "targets_0", "targets_1",
                    "offsets_0", "offsets_1", "fallThroughAddr", "is_br_sharing",
                    "br_taken_mask_0", "br_taken_mask_1"]
    for key in need_compare:
        assert_equal(uftb_output[key], std_output[key])

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
        self.s0_pc = 0
        self.s1_pc = 0
        self.s2_pc = 0
        self.s3_pc = 0
        self.s1_hit_way = 0
        self.s2_hit_way = 0
        self.s3_hit_way = 0

        self.ftq = FTQ()
        self.uftb_model = uFTBModel()
        self.ftb_provider = FTBProvider()

    def pipeline_assign(self):
        self.pipeline_ctrl.s0_fire_0.value = self.s0_fire
        self.pipeline_ctrl.s0_fire_1.value = self.s0_fire
        self.pipeline_ctrl.s0_fire_2.value = self.s0_fire
        self.pipeline_ctrl.s0_fire_3.value = self.s0_fire

        self.pipeline_ctrl.s1_fire_0.value = self.s1_fire
        self.pipeline_ctrl.s1_fire_1.value = self.s1_fire
        self.pipeline_ctrl.s1_fire_2.value = self.s1_fire
        self.pipeline_ctrl.s1_fire_3.value = self.s1_fire

        self.pipeline_ctrl.s2_fire_0.value = self.s2_fire
        self.pipeline_ctrl.s2_fire_1.value = self.s2_fire
        self.pipeline_ctrl.s2_fire_2.value = self.s2_fire
        self.pipeline_ctrl.s2_fire_3.value = self.s2_fire

        self.pipeline_ctrl.s3_fire_0.value = self.s3_fire
        self.pipeline_ctrl.s3_fire_1.value = self.s3_fire
        self.pipeline_ctrl.s3_fire_2.value = self.s3_fire
        self.pipeline_ctrl.s3_fire_3.value = self.s3_fire

        # Set the value to 1 forcibly to obtain meta information
        self.dut.io_s1_fire_0.value = 1
        self.dut.io_s2_fire_0.value = 1

        self.dut.io_in_bits_s0_pc_0.value = self.s0_pc
        self.dut.io_in_bits_s0_pc_1.value = self.s0_pc
        self.dut.io_in_bits_s0_pc_2.value = self.s0_pc
        self.dut.io_in_bits_s0_pc_3.value = self.s0_pc

    def generate_bpu_output(self, dut_output):
        dut_output["s1"]["valid"] = self.s1_fire
        dut_output["s2"]["valid"] = self.s2_fire
        dut_output["s3"]["valid"] = self.s3_fire

        dut_output["s2"]["pc_3"] = self.s2_pc
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
        self.enable_ctrl.ubtb_enable.value = 1
        self.s0_pc = RESET_VECTOR

        self.dut.reset.value = 1
        await ClockCycles(self.dut, 10)
        self.dut.reset.value = 0
        await ClockCycles(self.dut, 10)

        while True:
            self.pipeline_assign()
            await ClockCycles(self.dut, 1)

            self.s3_fire = self.s2_fire
            self.s2_fire = self.s1_fire
            self.s1_fire = self.s0_fire
            self.s3_pc = self.s2_pc
            self.s2_pc = self.s1_pc
            self.s1_pc = self.s0_pc
            self.s3_hit_way = self.s2_hit_way
            self.s2_hit_way = self.s1_hit_way

            npc_gen = self.s0_pc
            next_s0_fire = 1
            s1_flush = False
            s2_flush = False
            s3_flush = False


            # Get dut output and generate bpu output
            dut_output = self.dut_out.collect()
            bpu_output = self.generate_bpu_output(dut_output)

            ftb_entry = FTBEntry.from_full_pred_dict(self.s1_pc, dut_output["s1"]["full_pred"])
            model_output = self.uftb_model.generate_output(self.s1_fire, self.s1_pc)
            std_ftb_entry = self.ftb_provider.provide_ftb_entry(self.s1_fire, self.s1_pc)

            if model_output:
                self.s1_hit_way = model_output[2]
            else:
                self.s1_hit_way = None

            debug("-" * 30)
            if self.s1_fire:
                # Debug Imformation
                debug("[BPU]")
                debug(f"New prediction at {hex(self.s1_pc)}")
                if bpu_output["s1"]["full_pred"]["hit"]:
                    debug("Dut Hit")

                debug("FTB Entry in pred result: ")
                if bpu_output["s1"]["full_pred"]["hit"]:
                    debug(ftb_entry.__str__(self.s1_pc))
                else:
                    debug("No FTB Entry")
                debug(f"br_taken_mask: {bpu_output['s1']['full_pred']['br_taken_mask_0']}, {bpu_output['s1']['full_pred']['br_taken_mask_1']}")

                debug("FTB Entry in uFTB Model: ")
                if model_output:
                    debug(model_output[0].__str__(self.s1_pc))
                    debug(f"br_taken_mask: {model_output[1]}")
                else:
                    debug("No FTB Entry")

                # Compare dut output and uFTB model output
                expected_hit = model_output is not None
                actual_hit = bpu_output["s1"]["full_pred"]["hit"]
                assert_equal(expected_hit, actual_hit)
                if parse_uftb_meta(dut_output["last_stage_meta"])["hit"] or self.s3_hit_way is not None:
                    expected_hit_way = self.s3_hit_way
                    actual_hit_way = parse_uftb_meta(dut_output["last_stage_meta"])["pred_way"]
                    assert_equal(expected_hit_way, actual_hit_way)

                if model_output:
                    std_full_pred = {}
                    model_output[0].put_to_full_pred_dict(self.s1_pc, std_full_pred)
                    std_full_pred["br_taken_mask_0"] = model_output[1][0]
                    std_full_pred["br_taken_mask_1"] = model_output[1][1]
                    compare_uftb_full_pred(bpu_output["s1"]["full_pred"], std_full_pred)


            # Forward to FTQ and get update and redirect request
            if self.s1_fire:
                npc_gen = get_target_from_full_pred_dict(self.s1_pc, dut_output["s1"]["full_pred"])
            update_request, redirect_request = self.ftq.update(bpu_output, std_ftb_entry)

            ## Update Request
            if update_request:
                self.uftb_model.update(update_request)
                self.ftb_provider.update(update_request)
                self.dut_update.assign(update_request)
                self.dut_update.valid.value = 1
            else:
                self.dut_update.valid.value = 0

            ## Redirect Request
            if redirect_request:
                next_s0_fire = 1
                s1_flush = True
                s2_flush = True
                s3_flush = True
                npc_gen = redirect_request["cfiUpdate"]["target"]

            # Add new control information
            self.s0_fire = next_s0_fire
            self.s0_pc = npc_gen
            if s1_flush:
                self.s1_fire = 0
            if s2_flush:
                self.s2_fire = 0
            if s3_flush:
                self.s3_fire = 0
