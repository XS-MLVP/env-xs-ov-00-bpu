#!coding=utf8

import os
from .util import *
import time

class BRTParser:

    def __init__(self, check_trace=True) -> None:
        self.magic_head = b'\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe\xbe'
        self.magic_tail = b'\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed\xed'
        self.type_map = {
                   101 : "C.J",
                   102 : "C.JR",
                   103 : "C.CALL",
                   104 : "C.RET",
                   105 : "C.JALR",
                   201 : "P.JAL",
                   203 : "P.CALL",
                   204 : "P.RET",
                   0   : "*.CBR",
                   1   : "I.JAL",
                   2   : "I.JALR",
                   3   : "I.CALL",
                   4   : "I.RET",
                }
        self.logger = get_logger(self.__class__.__name__)
        self.check_trace = check_trace
        self.clear()

    def clear(self):
        self.branchs = {}
        self.branchs_step = []
        self.statistics_type = {}

    def disable_check(self):
        self.check_trace = False

    def enable_check(self):
        self.check_trace = True

    def parse_data(self, data):
        index  = int.from_bytes(data[0:8],   byteorder='little')
        pc     = int.from_bytes(data[8:16],  byteorder='little')
        target = int.from_bytes(data[16:24], byteorder='little')
        taken  = int.from_bytes(data[24:28], byteorder='little') > 0
        btype  = int.from_bytes(data[28:32], byteorder='little')
        if (btype not in self.type_map) and self.check_trace:
            self.logger.warning("Find Unrecognized Type: %d" % btype)
        btype  = self.type_map.get(btype, "ERROR-%s"%btype)
        key = pc
        return key, index, pc, target, taken, btype

    def load(self, file):
        if not os.path.isfile(file):
            self.logger.error("file: %s not find!" % file)
            return
        self.logger.debug("Load file: %s"%file)
        if not self.check_trace:
            self.logger.warning("Trace check is disabled!")
        time_start = time.time()
        with open(file, "rb") as fp:
            # read header
            header = fp.read(16)
            if(header != self.magic_head):
                self.logger.error("file[%s] is not a branch/jump trace")
                return
            pre_pc = -1
            while True:
                data = fp.read(32)
                if(data == self.magic_tail):
                    break
                key, index, pc, target, taken, btype = self.parse_data(data)
                if pc < pre_pc and self.check_trace:
                    self.logger.warning("Detect disordered PC (0x%x => 0x%x) sequence; potentially indicating a corrupted trace file." % (pre_pc, pc))
                if taken:
                    pre_pc = target
                if key not in self.branchs:
                    self.branchs[key] = {"pc": pc, "index": [index], "target": [target], "taken": [taken], "type": btype}
                    # statistic
                    if btype not in self.statistics_type:
                        self.statistics_type[btype] = {"count":1, "taken": int(taken), "notaken": int(not taken)}
                    else:
                        self.statistics_type[btype]["count"] += 1
                        self.statistics_type[btype]["taken"] += int(taken)
                        self.statistics_type[btype]["notaken"] += int(not taken)
                else:
                    self.branchs[key]["index"].append(index)
                    self.branchs[key]["target"].append(target)
                    self.branchs[key]["taken"].append(taken)
                    self.statistics_type[btype]["taken"] += int(taken)
                    self.statistics_type[btype]["notaken"] += int(not taken)

                self.branchs_step.append((index, self.branchs[key], len(self.branchs[key]["index"]) - 1))
        self.logger.debug("%d branchs (%d checks), loaded! time cost: %s"%(len(self.branchs), len(self.branchs_step), fmt_seconds(time.time() - time_start)))

    def fetch(self, file):
        from . import NemuBR as nbr
        nbr.br_monitor_init(["", "-b", file])
        while True:
            data = nbr.br_monitor_get()
            if data.index < 0:
                return None
            pc, index, target, taken, btype = data.pc, data.index, data.target,  data.taken, data.type
            if (btype not in self.type_map) and self.check_trace:
                self.logger.warning("Find Unrecognized Type: %d" % btype)
            btype  = self.type_map.get(btype, "ERROR-%s"%btype)
            if btype not in self.statistics_type:
                self.statistics_type[btype] = {"count":1, "taken": int(taken), "notaken": int(not taken)}
            else:
                self.statistics_type[btype]["count"] += 1
                self.statistics_type[btype]["taken"] += int(taken)
                self.statistics_type[btype]["notaken"] += int(not taken)
            yield {"pc": pc, "index": index, "target": target, "taken": taken, "type": btype}

    def print_stat(self):
        keys = self.statistics_type.keys()
        print("\n%5s %8s %8s %8s %8s" % ("Index", "Type", "icount", "taken", "notaken"))
        count, taken, notaken = 0, 0, 0
        all_cal, all_ret = 0, 0
        for i, k in enumerate(sorted(keys)):
            data = self.statistics_type[k]
            print("%5d %8s %8d %8d %8d" % (i, k, data["count"], data["taken"], data["notaken"]))
            count += data["count"]
            taken += data["taken"]
            notaken += data["notaken"]
            if ".RET" in k:
                all_ret += data["taken"]
            elif ".CALL" in k:
                all_cal += data["taken"]
        print("%5d %8s %8d %8d %8d (%d checks, ins.ret - ins.call = %d)\n" % (len(keys), "ALL", count, taken, notaken, taken + notaken, all_ret - all_cal))
