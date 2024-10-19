from mlvp import Bundle

class PipelineCtrlBundle(Bundle):
    signals = ["s0_fire_0", "s0_fire_1", "s0_fire_2", "s0_fire_3",
               "s1_fire_0", "s1_fire_1", "s1_fire_2", "s1_fire_3",
               "s2_fire_0", "s2_fire_1", "s2_fire_2", "s2_fire_3",
               "s3_fire_0", "s3_fire_1", "s3_fire_2", "s3_fire_3",
               "s1_ready", "s2_ready", "s3_ready",
               "s2_redirect", "s3_redirect"]
    
class IoInBundle(Bundle):
    signals = ["bits_s0_pc_0", "bits_s0_pc_1", "bits_s0_pc_2", "bits_s0_pc_3"]
    
class EnableCtrlBundle(Bundle):
    signals = ["ubtb_enable", "btb_enable", "bim_enable", "tage_enable",
               "sc_enable", "ras_enable", "loop_enable"]


class FTBEntryBundle(Bundle):
    signals = ["valid", "brSlots_0_offset", "brSlots_0_lower", "brSlots_0_tarStat", "brSlots_0_valid",
               "tailSlot_offset", "tailSlot_lower", "tailSlot_tarStat", "tailSlot_sharing", "tailSlot_valid",
               "pftAddr", "carry", "isCall", "isRet", "isJalr", "last_may_be_rvi_call",
               "always_taken_0", "always_taken_1"]

class UpdateBundle(Bundle):
    signals = ["valid", "bits_pc", "bits_br_taken_mask_0", "bits_br_taken_mask_1"]

    def __init__(self):
        super().__init__()
        self.ftb_entry = FTBEntryBundle.from_prefix("bits_ftb_entry_")

class FullBranchPredirectionBundle(Bundle):
    signals = ["hit", "slot_valids_0", "slot_valids_1", "targets_0", "targets_1",
               "offsets_0", "offsets_1", "fallThroughAddr", "fallThroughErr",
               "is_jal", "is_jalr", "is_call", "is_ret", "is_br_sharing",
               "last_may_be_rvi_call",
               "br_taken_mask_0", "br_taken_mask_1",
               "jalr_target"]

class BranchPredictionBundle(Bundle):
    signals = ["pc_0", "pc_1", "pc_2", "pc_3", "valid", "hasRedirect", "ftq_idx"]

    def __init__(self):
        super().__init__()
        self.full_pred = FullBranchPredirectionBundle.from_regex(r"full_pred_\d_(.*)")


class BranchPredictionResp(Bundle):
    signals = ["last_stage_meta"]

    def __init__(self):
        super().__init__()
        self.s1 = BranchPredictionBundle.from_prefix("s1_")
        self.s2 = BranchPredictionBundle.from_prefix("s2_")
        self.s3 = BranchPredictionBundle.from_prefix("s3_")
        self.last_stage_ftb_entry = FTBEntryBundle.from_prefix("last_stage_ftb_entry_")
