from .config import *

def get_slot_offset(pc, target):
    return ((target - pc) >> INST_OFFSET_BITS) & ((1 << PREDICT_WIDTH_OFFSET_BITS) - 1)

def get_slot_addr(pc, offset):
    return pc + (offset << INST_OFFSET_BITS)


def get_pftaddr(target):
    return (target >> INST_OFFSET_BITS) & ((1 << PREDICT_WIDTH_OFFSET_BITS) - 1)

def get_pftaddr_carry(pc, target):
    pc_higher = pc >> (INST_OFFSET_BITS + PREDICT_WIDTH_OFFSET_BITS)
    target_higher = target >> (INST_OFFSET_BITS + PREDICT_WIDTH_OFFSET_BITS)
    return (target_higher - pc_higher) & 1

def get_fallthrough_addr(pc, part_addr, carry):
    higher = (pc >> (INST_OFFSET_BITS + PREDICT_WIDTH_OFFSET_BITS)) + carry
    return (higher << (INST_OFFSET_BITS + PREDICT_WIDTH_OFFSET_BITS)) | (part_addr << INST_OFFSET_BITS)

def get_lower_addr(pc, bits):
    return (pc >> INST_OFFSET_BITS) & ((1 << bits) - 1)

def get_target_stat(pc_higher, target_higher):
    if target_higher < pc_higher:
        return TAR_UDF
    elif target_higher > pc_higher:
        return TAR_OVF
    else:
        return TAR_FIT

def get_target_addr(pc, target_stat, target_lower, target_lower_bits):
    target_higher = pc >> (target_lower_bits + INST_OFFSET_BITS)
    if target_stat == TAR_UDF:
        target_higher -= 1
    elif target_stat == TAR_OVF:
        target_higher += 1

    return (target_higher << (target_lower_bits + INST_OFFSET_BITS)) | (target_lower << INST_OFFSET_BITS)


def get_cfi_addr_from_full_pred_dict(pc, d):
    if not d["hit"]:
        return None
    elif d["slot_valids_0"] and d["br_taken_mask_0"]:
        return get_slot_addr(pc, d["offsets_0"])
    elif d["slot_valids_1"] and d["br_taken_mask_1"] and d["is_br_sharing"]:
        return get_slot_addr(pc, d["offsets_1"])
    elif d["slot_valids_1"] and not d["is_br_sharing"]:
        return get_slot_addr(pc, d["offsets_1"])
    else:
        return None

def get_target_from_full_pred_dict(pc, d):
    if not d["hit"]:
        return pc + PREDICT_WIDTH_BYTES
    elif d["slot_valids_0"] and d["br_taken_mask_0"]:
        return d["targets_0"]
    elif d["slot_valids_1"] and d["br_taken_mask_1"] and d["is_br_sharing"]:
        return d["targets_1"]
    elif d["slot_valids_1"] and not d["is_br_sharing"]:
        # return d["jalr_target"]
        return d["targets_1"]
    else:
        return d["fallThroughAddr"]

def set_all_none_item_to_zero(d):
    for k, v in d.items():
        if v is None:
            d[k] = 0

def parse_uftb_meta(meta):
    return {
        "pred_way": meta >> 1,
        "hit": meta & 1
    }

def gen_update_request(pc, new_ftb_entry, br_taken_mask, valid: bool = True):
    update_request = {}

    update_request["valid"] = valid
    update_request["bits_pc"] = pc
    update_request["ftb_entry"] = new_ftb_entry.__dict__()
    update_request["bits_br_taken_mask_0"] = 0 if len(br_taken_mask) == 0 else br_taken_mask[0]
    update_request["bits_br_taken_mask_1"] = 0 if len(br_taken_mask) < 2 else br_taken_mask[1]

    return update_request
        
