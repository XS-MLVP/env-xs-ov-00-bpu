from mlvp import Bundle

class PipelineCtrlBundle(Bundle):
    signals_list = ["s0_fire_0", "s0_fire_1", "s0_fire_2", "s0_fire_3",
                    "s1_fire_0", "s1_fire_1", "s1_fire_2", "s1_fire_3",
                    "s2_fire_0", "s2_fire_1", "s2_fire_2", "s2_fire_3",
                    "s3_fire_0", "s3_fire_1", "s3_fire_2", "s3_fire_3",
                    "s1_ready", "s2_ready", "s3_ready",
                    "s2_redirect", "s3_redirect"]

class EnableCtrlBundle(Bundle):
    signals_list = ["ubtb_enable", "btb_enable", "bim_enable", "tage_enable",
                    "sc_enable", "ras_enable", "loop_enable"]


class FTBEntryBundle(Bundle):
    signals_list = ["brSlots_0_offset", "brSlots_0_lower", "brSlots_0_tarStat", "brSlots_0_valid",
                    "tailSlot_offset", "tailSlot_lower", "tailSlot_tarStat", "tailSlot_sharing", "tailSlot_valid",
                    "pftAddr", "carry", "isCall", "isRet", "isJalr", "last_may_be_rvi_call",
                     "always_taken_0", "always_taken_1"]

class UpdateBundle(Bundle):
    signals_list = ["valid", "bits_pc", "bits_br_taken_mask_0", "bits_br_taken_mask_1"]

    sub_bundles = [
        ("ftb_entry", lambda dut: FTBEntryBundle.from_prefix(dut, "bits_ftb_entry_"))
    ]

class FullBranchPredirectionBundle(Bundle):
    signals_list = ["hit", "slot_valids_0", "slot_valids_1", "targets_0", "targets_1",
                    "offsets_0", "offsets_1", "fallThroughAddr", "fallThroughErr",
                    "is_jal", "is_jalr", "is_call", "is_ret", "is_br_sharing",
                    "last_may_be_rvi_call",
                    "br_taken_mask_0", "br_taken_mask_1",
                    "jalr_target"]

class BranchPredictionBundle(Bundle):
    signals_list = ["pc_3", "valid", "hasRedirect", "ftq_idx"]
    sub_bundles = [
        ("full_pred", lambda dut: FullBranchPredirectionBundle.from_regex(dut, r"full_pred_\d_(.*)"))
    ]


class BranchPredictionResp(Bundle):
    signals_list = ["last_stage_meta"]
    sub_bundles = [
        ("s1", lambda dut: BranchPredictionBundle.from_prefix(dut, "s1_")),
        ("s2", lambda dut: BranchPredictionBundle.from_prefix(dut, "s2_")),
        ("s3", lambda dut: BranchPredictionBundle.from_prefix(dut, "s3_")),
        ("last_stage_ftb_entry", lambda dut: FTBEntryBundle.from_prefix(dut, "last_stage_ftb_entry_"))
    ]
