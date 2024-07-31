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

        # print(self.pipeline_ctrl.s1_fire_0.value, self.s3_fire)

        assert_equal(self.dut.io_s0_fire_0.value, self.s0_fire)
        assert_equal(self.dut.io_s0_fire_1.value, self.s0_fire)
        assert_equal(self.dut.io_s0_fire_2.value, self.s0_fire)
        assert_equal(self.dut.io_s0_fire_3.value, self.s0_fire)

        assert_equal(self.dut.io_s1_fire_0.value, self.s1_fire)
        assert_equal(self.dut.io_s1_fire_1.value, self.s1_fire)
        assert_equal(self.dut.io_s1_fire_2.value, self.s1_fire)
        assert_equal(self.dut.io_s1_fire_3.value, self.s1_fire)

        assert_equal(self.dut.io_s2_fire_0.value, self.s2_fire)
        assert_equal(self.dut.io_s2_fire_1.value, self.s2_fire)
        assert_equal(self.dut.io_s2_fire_2.value, self.s2_fire)
        assert_equal(self.dut.io_s2_fire_3.value, self.s2_fire)

        # Set the value to 1 forcibly to obtain meta information
        # self.dut.io_s1_fire_0.value = 1
        # self.dut.io_s2_fire_0.value = 1


        self.dut.io_in_bits_s0_pc_0.value = self.s0_pc
        self.dut.io_in_bits_s0_pc_1.value = self.s0_pc
        self.dut.io_in_bits_s0_pc_2.value = self.s0_pc
        self.dut.io_in_bits_s0_pc_3.value = self.s0_pc

        assert_equal(self.dut.io_in_bits_s0_pc_0.value, self.s0_pc)
        assert_equal(self.dut.io_in_bits_s0_pc_1.value, self.s0_pc)
        assert_equal(self.dut.io_in_bits_s0_pc_2.value, self.s0_pc)
        assert_equal(self.dut.io_in_bits_s0_pc_3.value, self.s0_pc)

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
        ftb_provider_stage_enable = (False, True, True)

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
        self.enable_ctrl.btb_enable.value = 1
        self.s0_pc = RESET_VECTOR

        self.dut.reset.value = 1
        await ClockCycles(self.dut, 10)
        self.dut.reset.value = 0
        await ClockCycles(self.dut, 10)

        while True:
            self.pipeline_assign()
            await ClockCycles(self.dut, 1)
            debug("========tick========")

            self.ftb_model.process_update()

            self.s3_fire = self.s2_fire
            self.s2_fire = self.s1_fire
            self.s1_fire = self.s0_fire
            self.s3_pc = self.s2_pc
            self.s2_pc = self.s1_pc
            self.s1_pc = self.s0_pc
            self.s3_hit_way = self.s2_hit_way
            self.s2_hit_way = self.s1_hit_way
            
            debug(f"{self.s0_fire} {self.s1_fire} {self.s2_fire} {self.s3_fire}")

            npc_gen = self.s0_pc
            next_s0_fire = 1
            s1_flush = False
            s2_flush = False
            s3_flush = False

            # Get dut output and generate bpu output
            dut_output = self.dut_out.as_dict()
            # debug(dut_output)
            bpu_output = self.generate_bpu_output(dut_output)
            # test input
            dut_input = self.io_in.as_dict()

            ftb_entry = FTBEntry.from_full_pred_dict(self.s2_pc, dut_output["s2"]["full_pred"])
            model_output = self.ftb_model.generate_output(self.s0_fire, 
                                                          self.s1_fire,
                                                          self.s2_fire, 
                                                          self.s2_pc)
            std_ftb_entry = self.ftb_provider.provide_ftb_entry(self.s2_fire, self.s2_pc)

            
            if model_output is not None:
                self.s2_hit_way = model_output[1]
            else:
                self.s2_hit_way = None

            if self.s2_fire:
                # Compare dut output and uFTB model output
                actual_hit = bool(bpu_output["s2"]["full_pred"]["hit"])
                # info(bpu_output["s2"]["full_pred"]["hit"])
                expected_hit = model_output is not None
                assert_equal(actual_hit, expected_hit)

                if model_output:
                    std_full_pred = {}
                    model_output[0].put_to_full_pred_dict(self.s2_pc, std_full_pred)
                    # std_full_pred["br_taken_mask_0"] = model_output[1][0]
                    # std_full_pred["br_taken_mask_1"] = model_output[1][1]
                    compare_uftb_full_pred(bpu_output["s2"]["full_pred"], std_full_pred)

            if self.s3_fire:
                if parse_uftb_meta(dut_output["last_stage_meta"])["hit"] or self.s1_hit_way is not None:
                    actual_hit_way = parse_uftb_meta(dut_output["last_stage_meta"])["pred_way"]
                    debug(f"Dut_output last_stage_meta pred_way {actual_hit_way}")
                    expected_hit_way = 0 if self.s1_hit_way is None else self.s1_hit_way
                    assert_equal(actual_hit_way, expected_hit_way)

            # Forward to FTQ and get update and redirect request
            if self.s2_fire:
                npc_gen = get_target_from_full_pred_dict(self.s2_pc, dut_output["s2"]["full_pred"])
            update_request, redirect_request = self.ftq.update(bpu_output, std_ftb_entry)

            ## Update Request
            if update_request:
                self.ftb_model.update(update_request)
                self.ftb_provider.update(update_request)
                if update_request["bits_meta"] is None:
                    update_request["bits_meta"] = 0
                del update_request['bits_br_taken_mask_0']
                del update_request['bits_br_taken_mask_1']
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
