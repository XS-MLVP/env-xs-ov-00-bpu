

import sys
import time
from datetime import datetime

def fmt_time(t = None, fmt="%Y-%m-%d %H:%M:%S"):
    if t is None:
        t = time.time()
    return datetime.fromtimestamp(t).strftime(fmt)

def fmt_seconds(t: float):
    if t == 0:
        return "0 seconds"
    ret = ""
    for d, f, u in [(60, " %.2f", "second"), (60, " %d", "minute"), (24, " %d", "hour"), (sys.maxsize, " %d", "day")]:
        if t == 0:
            break
        v = t % d
        t = t // d
        ret = (f + " %s%s")%(v, u, "" if v == 1 else "s")  + ret
    return ret.strip()


