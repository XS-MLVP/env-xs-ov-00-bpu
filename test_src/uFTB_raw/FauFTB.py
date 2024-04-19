from typing import Any, Tuple
from UT_FauFTB import *
from FTBEntry import *
from collections import namedtuple


class FauFTB(DUTFauFTB):

    class Io_in_bits_s0_pc:

        def __init__(self, outer_instance: "FauFTB"):
            self.outer_instance = outer_instance
            for i in range(4):
                setattr(self, f"_{i}", getattr(outer_instance, f"io_in_bits_s0_pc_{i}"))

        def set(self, arg):
            for i in range(4):
                getattr(self, f"_{i}").value = arg

    class Io_out_s1_pc:

        def __init__(self, outer_instance: "FauFTB"):
            self.outer_instance = outer_instance
            for i in range(4):
                setattr(self, f"_{i}", getattr(outer_instance, f"io_out_s1_pc_{i}"))

        def get(self):
            assert all(self._0.value == getattr(self, f"_{i}").value for i in range(4))
            return self._0

    class Io_s0_fire:

        def __init__(self, outer_instance: "FauFTB"):
            self.outer_instance = outer_instance
            for i in range(4):
                setattr(self, f"_{i}", getattr(outer_instance, f"io_s0_fire_{i}"))

        def set(self,arg):
            for i in range(4):
                getattr(self, f"_{i}").value = arg

    class Io_out_s1_full_pred:

        def __init__(self, outer_instance: "FauFTB"):
            self.outer_instance = outer_instance
            self.sig_array = [
                "br_taken_mask_0",
                "br_taken_mask_1",
                "slot_valids_0",
                "slot_valids_1",
                "targets_0",
                "targets_1",
                "offsets_0",
                "offsets_1",
                "fallThroughAddr",
                "is_br_sharing",
                "hit",
            ]
            for i in range(4):
                setattr(
                    self,
                    f"_{i}",
                    namedtuple(f"_{i}", self.sig_array)(
                        *[
                            getattr(outer_instance, f"io_out_s1_full_pred_{i}_{sig}")
                            for sig in self.sig_array
                        ]
                    ),
                )

        def get(self):
            for sig in self.sig_array:
                assert all(
                    getattr(self, f"_{i}")._asdict()[sig].value
                    == getattr(self, f"_{i}")._asdict()[sig].value
                    for i in range(4)
                )
            return self._0

    class Io_out_last_stage_meta:

        def __init__(self, outer_instance: "FauFTB"):
            self.outer_instance = outer_instance

            self.resp_meta_hit_r_1 = xsp.XPin(
                outer_instance.io_out_last_stage_meta.xdata.SubDataRef(
                    "resp_meta_hit_r_1",
                    0,
                    0
                ),
                outer_instance.event,
            )

            self.resp_meta_pred_way_r_1 = xsp.XPin(
                outer_instance.io_out_last_stage_meta.xdata.SubDataRef(
                    "resp_meta_pred_way_r_1",
                    1,
                    5
                ),
                outer_instance.event,
            )

            pass

        pass

    class Io_update_bits_ftb_entry:

        def __init__(self, outer_instance: "FauFTB"):
            self.outer_instance = outer_instance
            self.sig_array = [
                "brSlots_0_valid",
                "brSlots_0_offset",
                "brSlots_0_lower",
                "brSlots_0_tarStat",
                "always_taken_0",
                "tailSlot_valid",
                "tailSlot_offset",
                "tailSlot_lower",
                "tailSlot_tarStat",
                "tailSlot_sharing",
                "always_taken_1",
                "pftAddr",
                "carry",
            ]
            namedtuple(
                "Io_update_bits_ftb_entry",
                self.sig_array,
            )(
                *[
                    setattr(
                        self,
                        sig,
                        getattr(outer_instance, f"io_update_bits_ftb_entry_{sig}"),
                    )
                    for sig in self.sig_array
                ]
            )

    def __init__(self):
        super().__init__()
        self.io_in_bits_s0_pc = self.Io_in_bits_s0_pc(self)
        self.io_out_s1_pc = self.Io_out_s1_pc(self)
        self.io_s0_fire = self.Io_s0_fire(self)
        self.io_out_s1_full_pred = self.Io_out_s1_full_pred(self)
        self._io_out_last_stage_meta = self.Io_out_last_stage_meta(self)
        self.io_update_bits_ftb_entry = self.Io_update_bits_ftb_entry(self)
        self.init_clock("clock")

    def finalize(self):
        super().finalize()

    def check_dup_equation(self, *inputs):
        return all(i == inputs[0] for i in inputs)

    def s1_full_pred(self) -> Tuple[int, FTBEntry, int, int]:
        io_out_s1_full_pred = self.io_out_s1_full_pred.get()

        entry = FTBEntry()

        # FauFTB
        entry.valid = io_out_s1_full_pred.hit.value
        entry.pftAddr = io_out_s1_full_pred.fallThroughAddr.value
        # Br slot
        entry.brSlot.valid = io_out_s1_full_pred.slot_valids_0.value
        entry.brSlot.offset = io_out_s1_full_pred.offsets_0.value
        entry.brSlot.target = io_out_s1_full_pred.targets_0.value
        entry.brSlot.targetCoA = None
        entry.brSlot.alwaysTaken = io_out_s1_full_pred.br_taken_mask_0.value
        # Tail slot
        entry.tailSlot.valid = io_out_s1_full_pred.slot_valids_1.value
        entry.tailSlot.offset = io_out_s1_full_pred.offsets_1.value
        entry.tailSlot.target = io_out_s1_full_pred.targets_1.value
        entry.tailSlot.targetCoA = None
        entry.tailSlot.alwaysTaken = io_out_s1_full_pred.br_taken_mask_1.value
        entry.tailSlot.is_br_sharing = io_out_s1_full_pred.is_br_sharing.value

        return (self.io_out_s1_pc.get().value, entry, io_out_s1_full_pred.br_taken_mask_0.value, io_out_s1_full_pred.br_taken_mask_1.value)

    def update_ftb_entry(self, update_pc: int, entry: FTBEntry, taken: Tuple[int, int]):

        self.io_update_bits_pc.value = update_pc
        self.io_update_bits_br_taken_mask_0.value = taken[0]
        self.io_update_bits_br_taken_mask_1.value = taken[1]

        update = self.io_update_bits_ftb_entry

        update.brSlots_0_valid.value = entry.brSlot.valid
        update.brSlots_0_offset.value = entry.brSlot.offset
        update.brSlots_0_lower.value = entry.brSlot.target
        update.brSlots_0_tarStat.value = entry.brSlot.targetCoA
        update.always_taken_0.value = entry.brSlot.alwaysTaken

        update.tailSlot_valid.value = entry.tailSlot.valid
        update.tailSlot_offset.value = entry.tailSlot.offset
        update.tailSlot_lower.value = entry.tailSlot.target
        update.tailSlot_tarStat.value = entry.tailSlot.targetCoA
        update.tailSlot_sharing.value = entry.tailSlot.is_br_sharing
        update.always_taken_1.value = entry.tailSlot.alwaysTaken

        update.pftAddr.value = entry.pftAddr
        update.carry.value = entry.carry
