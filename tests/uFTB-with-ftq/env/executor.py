from .config import *

import os
os.sys.path.append(UTILS_PATH)

from BRTParser import BRTParser

class Executor:
    """Get program real execution instruction flow."""

    def __init__(self, filename, reset_vector=0x80000000):
        self._executor = BRTParser().fetch(filename)
        self._current_branch = next(self._executor)
        self._current_pc = reset_vector

        self._last_exec_result = {
            "pc": 0,
            "inst_len": 0,
            "branch": 0
        }

        self._exec_once()

    def current_inst(self):
        """Return current instruction information."""
        return self._last_exec_result["pc"], self._last_exec_result["inst_len"], self._last_exec_result["branch"]

    def next_inst(self):
        """Move to next instruction."""
        self._exec_once()

    def _exec_once(self):
        # print(f"- Executor: pc: {hex(self._last_exec_result['pc'])}, inst_len: {self._last_exec_result['inst_len']},\
                # branch: {self._last_exec_result['branch']}")

        self._last_exec_result["pc"] = self._current_pc

        inst_len, branch = 0, None
        if (2 <= self._current_branch["pc"] - self._current_pc <= 4):
            inst_len = self._current_branch["pc"] - self._current_pc
            self._current_pc = self._current_branch["pc"]

        elif (self._current_branch["pc"] == self._current_pc):
            inst_len = Executor.branch_inst_len(self._current_branch)
            self._current_pc = self._current_branch["target"] if self._current_branch["taken"] \
                else self._current_pc + inst_len

            branch = self._current_branch
            self._current_branch = next(self._executor)

        else:
            inst_len = Executor.random_inst_len(self._current_pc)
            self._current_pc += Executor.random_inst_len(self._current_pc)

        self._last_exec_result["inst_len"] = inst_len
        self._last_exec_result["branch"] = branch

    @staticmethod
    def random_inst_len(pc):
        xor_ans = 0
        for i in range(8):
            xor_ans ^= (pc >> i) & 1
        return 2 if xor_ans else 4

    @staticmethod
    def is_cond_branch_inst(branch):
        return branch["type"] == "*.CBR"

    @staticmethod
    def is_jump_inst(branch):
        return not Executor.is_cond_branch_inst(branch)

    @staticmethod
    def is_call_inst(branch):
        return ".CALL" in branch["type"]

    @staticmethod
    def is_ret_inst(branch):
        return ".RET" in branch["type"]

    @staticmethod
    def is_jal_inst(branch):
        return branch["type"] == "I.JAL" or branch["type"] == "P.JAL"

    @staticmethod
    def is_jalr_inst(branch):
        return ".JALR" in branch["type"] or ".JR" in branch["type"]

    @staticmethod
    def is_compressed_inst(branch):
        type = branch["type"]
        if "C." in type:
            return True
        elif Executor.is_cond_branch_inst(branch):
            return Executor.random_inst_len(branch["pc"]) == 2
        else:
            return False

    @staticmethod
    def branch_inst_len(branch):
        return 2 if Executor.is_compressed_inst(branch) else 4

