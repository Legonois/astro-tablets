import os
import subprocess
import sys
from collections import OrderedDict
from typing import Callable, List, Optional, TypeVar

from skyfield.timelib import Time, Timescale

PROGRESS_CALLBACK = Optional[Callable[[float], None]]


def diff_mins(t1: Time, t2: Time) -> float:
    jdiff = abs(t1 - t2)
    mins_in_day = 60 * 24
    return jdiff * mins_in_day


def diff_hours(t1: Time, t2: Time) -> float:
    jdiff = abs(t1 - t2)
    return jdiff * 24


def diff_time_degrees_signed(t1: float, t2: float) -> float:
    jdiff = t1 - t2
    degrees_in_day = 360
    return jdiff * degrees_in_day


def same_sign(num1, num2) -> bool:
    return (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0)


def print_progress(prefix: str, progress: float):
    if progress > 0.99:
        progress = 1
    sys.stdout.write(f"\r{prefix}{progress * 100:05.2f}%")
    sys.stdout.flush()


def change_in_longitude(old: float, new: float) -> float:
    """
    For longitudes that wraps around 360 degrees.
    Find the smallest signed difference
    """
    assert 0 <= old <= 360
    assert 0 <= new <= 360
    a = new - old
    b = (360 - old) + new if old > new else -old - (360 - new)
    if abs(a) < abs(b):
        return a
    else:
        return b


def get_git_hash() -> str:
    hash = os.getenv("GIT_HASH")
    if hash is not None and len(hash) > 0:
        return hash
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
            .decode("utf-8")
            .partition("\n")[0]
        )
    except subprocess.CalledProcessError:
        return "unknown"


def get_git_changes() -> bool:
    modified = os.getenv("GIT_MODIFIED")
    if modified is not None:
        return modified == "1"
    try:
        subprocess.check_output(["git", "diff", "--exit-code"], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return True
    return False


E = TypeVar("E")
K = TypeVar("K")


def array_group_by(input: List[E], key_fn: Callable[[E], K]) -> OrderedDict[K, List[E]]:
    res: OrderedDict[K, List[E]] = OrderedDict()
    for item in input:
        key = key_fn(item)
        if key in res:
            res[key].append(item)
        else:
            res[key] = [item]
    return res


class TimeValue:
    def __init__(self, inner: float):
        self.inner = inner

    def string(self, timescale: Timescale):
        if self.inner is None:
            return ""
        t = timescale.tt_jd(self.inner + 3 / 24)
        return "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*t.ut1_calendar())

    def __eq__(self, other):
        if isinstance(other, TimeValue):
            return self.inner == other.inner
        return False
