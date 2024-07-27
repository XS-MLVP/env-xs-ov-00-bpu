from mlvp.modules import PLRU, TwoBitsCounter
from .ftb_bank import *

class uFTBModel:
    def __init__(self):
        self.replacer = PLRU(FTB_BANK_WAYS_NUM * FTB_BANK_SETS_NUM)
        self.ftbbank = FTBBank()
        self.counters = [[TwoBitsCounter(), TwoBitsCounter()] for _ in range(FTB_BANK_WAYS_NUM * FTB_BANK_SETS_NUM)]

        # Update requests are used to update FTBways and counters.
        self.update_queue = []

        # The update queue of the replacement algorithm, and there are two channels,
        # the first channel has a higher priority.
        self.replacer_update_queue = [[], []]

    def update(self, update_request):
        self.update_queue.append((update_request, 2, None))