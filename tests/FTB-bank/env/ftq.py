from mlvp import *
from random import random
from .bundle import *
from .config import *
from .utils import *
from .executor import Executor
from .ftb_way import *

class PredictionStatistician:
    """Predictive condition statistician for branch instructions"""

    def __init__(self):
        # { pc : [number, right_number]}
        self.cond_branches_list = {}

        # { pc : [type, number, right_number]}
        self.jmp_branches_list = {}


    def record_cond_branch(self, pc, correct):
        if pc in self.cond_branches_list:
            self.cond_branches_list[pc][0] += 1
            self.cond_branches_list[pc][1] += correct
        else:
            self.cond_branches_list[pc] = [1, int(correct)]

    def record_jmp_branch(self, pc, branch_type, correct):
        if pc in self.jmp_branches_list:
            self.jmp_branches_list[pc][1] += 1
            self.jmp_branches_list[pc][2] += correct
        else:
            self.jmp_branches_list[pc] = [branch_type, 1, int(correct)]

    def summary(self):
        summary_str = ""
        summary_str += "=" * 30 + "\n"
        summary_str += "Summary\n"
        summary_str += "[Conditional Branches]\n"
        cond_branches_total = sum([record[0] for record in self.cond_branches_list.values()])
        cond_branches_correct = sum([record[1] for record in self.cond_branches_list.values()])
        summary_str += f"Total: {cond_branches_total}, Correct: {cond_branches_correct}, Accuracy: {cond_branches_correct / max(1,cond_branches_total)}\n"

        for pc, record in self.cond_branches_list.items():
            summary_str += f"PC: {hex(pc)}\tTotal: {record[0]}\tCorrect: {record[1]}\tAccuracy: {record[1] / record[0]}\n"

        summary_str += "[Jump Branches]\n"
        jmp_branches_total = sum([record[1] for record in self.jmp_branches_list.values()])
        jmp_branches_correct = sum([record[2] for record in self.jmp_branches_list.values()])
        summary_str += f"Total: {jmp_branches_total}, Correct: {jmp_branches_correct}, Accuracy: {jmp_branches_correct / max(1,jmp_branches_total)}\n"
        for pc, record in self.jmp_branches_list.items():
            summary_str += f"PC: {hex(pc)}\tType: {record[0]}\tTotal: {record[1]}\tCorrect: {record[2]}\tAccuracy: {record[2] / max(1,record[1])}\n"

        summary_str += "[All Branches]\n"
        total = cond_branches_total + jmp_branches_total
        correct = cond_branches_correct + jmp_branches_correct
        summary_str += f"Total: {total}, Correct: {correct}, Accuracy: {correct /max(1, total)}\n"

        info(summary_str)

    @staticmethod
    def get_type(is_call, is_ret, is_jalr, is_jal):
        if is_call:
            return "call"
        elif is_ret:
            return "ret"
        elif is_jalr:
            return "jalr"
        elif is_jal:
            return "jal"
        else:
            return "jmp"

pred_stat = PredictionStatistician()



class FTQEntry:
    """Stores all the information that FTQ entries need to record."""

    def __init__(self):
        self.pc = None
        self.ftb = None
        self.full_pred = None
        self.meta = None

class FTQ:
    """Simulate FTQ behavior."""

    def __init__(self):
        self.executor = Executor(filename=PROGRAM_PATH, reset_vector=RESET_VECTOR)

        self.entries = [FTQEntry() for _ in range(32)]
        self.bpu_ptr = 0
        self.exec_ptr = 0

        self.update_queue = []
        self.redirect_queue = []

    def update(self, bpu_out, ftb_entry):
        # print("[FTQ]")

        # Get the result from BPU out and update the FTQ entry
        self._update_entries(bpu_out, ftb_entry)

        # Execute a FTQ entry
        self._exec_one_ftq_entry()

        # Generate update and redirect request
        update_request, redirect_request = None, None
        if self.update_queue:
            update_request = self._generate_update_request(self.update_queue.pop(0))
            # debug(f"Send Update Request: {hex(update_request['bits_pc'])} br_taken_mask: {update_request['bits_br_taken_mask_0']}, {update_request['bits_br_taken_mask_1']}")
        if self.redirect_queue:
            cfi_target = self.redirect_queue.pop(0)
            redirect_request = self._generate_redirect_request(cfi_target)
            debug("Send Redirect Request: (target: %s)" % hex(cfi_target))

        # if update_request is not None:
        #     update_request["ftb_entry"]["valid"] = update_request["ftb_entry"]["brSlots_0_valid"] or update_request["ftb_entry"]["tailSlot_valid"]

        return (update_request, redirect_request)

    def _get_entry(self, ptr):
        return self.entries[ptr % 32]

    def _exec_one_ftq_entry(self):
        if self.exec_ptr >= self.bpu_ptr:
            return None

        # Get a FTQ entry
        entry = self._get_entry(self.exec_ptr)
        executor_current_pc = self.executor.current_inst()[0]
        self.exec_ptr += 1
        debug("Executing FTQ entry at pc %s" % hex(entry.pc))

        # Prediction Block Hit
        if entry.full_pred["hit"] and entry.pc == executor_current_pc:
            debug("Prediction Block Hit")

            # Execute the prediction block
            all_branches, redirect_addr, br_taken_mask = self._execute_this_pred_block(entry.pc, entry.full_pred)
            if redirect_addr is None:
                debug("Predicition is correct")
            else:
                debug("Prediction is wrong, redirect to %s" % hex(redirect_addr))
            new_ftb_entry = self._update_ftb_entry_from_branches(entry.pc, entry.ftb, all_branches, br_taken_mask)
            self.update_queue.append((entry.pc, new_ftb_entry, br_taken_mask, entry.meta))
            if redirect_addr is not None:
                self.redirect_queue.append((redirect_addr))

        # Prediction Block Miss
        else:
            debug("Prediction Block Miss")
            if entry.pc != executor_current_pc:
                debug("Target Error: actual: %s expected: %s" % (hex(entry.pc), hex(executor_current_pc)))

            # Create a new FTB entry and update & redirect
            new_ftb_entry, br_taken_mask = self._generate_new_ftb_entry(executor_current_pc)
            self.update_queue.append((executor_current_pc, new_ftb_entry, br_taken_mask, entry.meta))
            self.redirect_queue.append((self.executor.current_inst()[0]))

    def _generate_update_request(self, update_queue_item):
        pc = update_queue_item[0]
        new_ftb_entry = update_queue_item[1]
        br_taken_mask = update_queue_item[2]
        meta = update_queue_item[3]
        # old_entry = update_queue_item[4]
        update_request = {}

        update_request["valid"] = True
        update_request["bits_pc"] = pc
        update_request["ftb_entry"] = new_ftb_entry.__dict__()
        # update_request["old_entry"] = old_entry
        update_request["bits_meta"] = meta
        update_request["bits_br_taken_mask_0"] = 0 if len(br_taken_mask) == 0 else br_taken_mask[0]
        update_request["bits_br_taken_mask_1"] = 0 if len(br_taken_mask) < 2 else br_taken_mask[1]

        return update_request

    def _generate_redirect_request(self, cfi_target):
        redirect_request = {}
        redirect_request["cfiUpdate"] = {}
        redirect_request["cfiUpdate"]["target"] = cfi_target

        return redirect_request

    def _update_ftb_entry_from_branches(self, pc, ftb_entry, branches, br_taken_mask):
        # update always_taken
        if len(br_taken_mask) >= 1:
            ftb_entry.always_taken[0] &= br_taken_mask[0]
        if len(br_taken_mask) >= 2:
            ftb_entry.always_taken[1] &= br_taken_mask[1]

        # update jmp target
        for branch in branches:
            if Executor.is_jump_inst(branch):
                ftb_entry.tailSlot.lower = get_lower_addr(branch["target"], 20)
                ftb_entry.tailSlot.tarStart = get_target_stat(pc >> 20, branch["target"] >> 20)

        return ftb_entry

    def _record_branch_helper(self, branch, cfi_addr, cfi_target):
        if Executor.is_cond_branch_inst(branch):
            correct = None
            if branch["taken"]:
                correct = cfi_addr is not None and branch["pc"] == cfi_addr
            else:
                correct = cfi_addr is None or branch["pc"] != cfi_addr
            pred_stat.record_cond_branch(branch["pc"], correct)
        else:
            correct = cfi_addr is not None and branch["pc"] == cfi_addr and branch["target"] == cfi_target
            pred_stat.record_jmp_branch(branch["pc"], PredictionStatistician.get_type(Executor.is_call_inst(branch),
                                            Executor.is_ret_inst(branch),
                                            Executor.is_jalr_inst(branch),
                                            Executor.is_jal_inst(branch)),
                                            correct)

    def _execute_this_pred_block(self, pc, full_pred):
        end_pc = full_pred["fallThroughAddr"]
        cfi_addr = get_cfi_addr_from_full_pred_dict(pc, full_pred)
        cfi_target = get_target_from_full_pred_dict(pc, full_pred)

        all_branches = []
        br_taken_mask = []
        redirect_addr = None
        while pc < end_pc:
            _, inst_len, branch = self.executor.current_inst()
            self.executor.next_inst()
            if branch is not None:
                br_taken_mask.append(branch["taken"])
                all_branches.append(branch)
                self._record_branch_helper(branch, cfi_addr, cfi_target)

            pred_cfi_valid = cfi_addr is not None and pc == cfi_addr
            exec_cfi_valid = branch is not None and branch["taken"]
            pc += inst_len

            if pred_cfi_valid and exec_cfi_valid:
                if cfi_target != branch["target"]:
                    redirect_addr = branch["target"]
                break
            elif pred_cfi_valid and not exec_cfi_valid:
                redirect_addr = pc
                break
            elif not pred_cfi_valid and exec_cfi_valid:
                redirect_addr = branch["target"]
                break

        return all_branches, redirect_addr, br_taken_mask

    def _generate_new_ftb_entry(self, pc):
        br_taken_mask = []
        ftb_entry = FTBEntry()

        fallthrough_addr = pc
        while fallthrough_addr < pc + PREDICT_WIDTH_BYTES:
            _, inst_len, branch = self.executor.current_inst()

            if branch is not None:
                if Executor.is_cond_branch_inst(branch):
                    success = ftb_entry.add_cond_branch_inst(pc, branch["pc"], branch["taken"], branch["target"])
                    br_taken_mask.append(branch["taken"])

                    if not success:
                        break
                    else:
                        pred_stat.record_cond_branch(branch["pc"], False)
                        self.executor.next_inst()
                        fallthrough_addr += inst_len
                        if branch["taken"]:
                            break
                else:
                    success = ftb_entry.add_jmp_inst(pc,
                                                  branch["pc"],
                                                  branch["target"],
                                                  inst_len,
                                                  Executor.is_call_inst(branch),
                                                  Executor.is_ret_inst(branch),
                                                  Executor.is_jalr_inst(branch),
                                                  Executor.is_jal_inst(branch))
                    if success:
                        pred_stat.record_jmp_branch(branch["pc"], PredictionStatistician.get_type(Executor.is_call_inst(branch),
                            Executor.is_ret_inst(branch),
                            Executor.is_jalr_inst(branch),
                            Executor.is_jal_inst(branch)),
                            False)
                        fallthrough_addr += 2
                        self.executor.next_inst()

                    break
            else:
                fallthrough_addr += inst_len
                self.executor.next_inst()

        ftb_entry.valid = True
        ftb_entry.pftAddr = get_pftaddr(fallthrough_addr)
        ftb_entry.carry = get_pftaddr_carry(pc, fallthrough_addr)

        debug("Generate FTB Entry")
        # debug(ftb_entry.__str__(pc))

        return ftb_entry, br_taken_mask

    def _update_entries(self, bpu_out, ftb_entry):
        if bpu_out["s2"]["valid"]:
            debug("Add ftq entry (pc: %s)" % hex(bpu_out["s2"]["pc_3"]))
            entry = self._get_entry(self.bpu_ptr)
            entry.full_pred = bpu_out["s2"]["full_pred"]
            entry.pc = bpu_out["s2"]["pc_3"]
            entry.ftb = ftb_entry
            entry.meta = bpu_out["last_stage_meta"]
            self.bpu_ptr += 1



if __name__ == "__main__":
    parser = Executor()
    for _ in range (100):
        print(parser.current_inst())
        parser.next_inst()

