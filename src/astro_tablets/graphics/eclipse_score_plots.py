import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import Precision
from astro_tablets.query.database import LunarEclipse
from astro_tablets.query.lunar_eclipse_query import (
    CompositePhaseTiming,
    FirstContactRelative,
    FirstContactTime,
    LunarEclipseQuery,
)
from astro_tablets.util import diff_time_degrees_signed


def plot_eclipse_time_of_day_score(dest: str):
    eclipse = LunarEclipse(
        sunrise=1458133.8958227257,
        partial_eclipse_begin=1458133.9258227257,
        e_type="",
        closest_approach_time=0,
        onset_us=0,
        maximal_us=0,
        clearing_us=0,
        sum_us=0,
        visible=False,
        angle=0,
        position=None,
        sunset=0,
    )
    assert eclipse.partial_eclipse_begin is not None
    actual = diff_time_degrees_signed(eclipse.partial_eclipse_begin, eclipse.sunrise)

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Observed Time After Sunrise (UŠ)")
    ax1.set_ylabel("Score")

    xs = np.arange(-15, 25, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_time_of_day_score(
                eclipse,
                FirstContactTime(x, FirstContactRelative.AFTER_SUNRISE),
                Precision.REGULAR,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Regular Precision", color="b")

    xs = np.arange(-15, 25, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_time_of_day_score(
                eclipse,
                FirstContactTime(x, FirstContactRelative.AFTER_SUNRISE),
                Precision.LOW,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Low Precision", color="g")

    ax1.axvline(x=actual, color="r", label="Expected Time")
    ax1.legend()

    plt.savefig(dest)


def plot_eclipse_phase_length_score(dest: str):
    eclipse = LunarEclipse(
        sunrise=0,
        partial_eclipse_begin=0,
        e_type="",
        closest_approach_time=0,
        onset_us=0,
        maximal_us=0,
        clearing_us=0,
        sum_us=62.75,
        visible=False,
        angle=0,
        position=None,
        sunset=0,
    )
    xs = np.arange(40, 80, 0.01)
    ys = list(
        map(
            lambda x: LunarEclipseQuery.eclipse_phase_length_score(
                eclipse, CompositePhaseTiming(x)
            ),
            xs,
        )
    )

    f, ax1 = plt.subplots()
    ax1.set_xlabel("Observed Eclipse Total Length (UŠ)")
    ax1.set_ylabel("Score")
    ax1.plot(xs, ys)
    ax1.axvline(x=eclipse.sum_us, color="r", label="Expected Length")
    ax1.legend()

    plt.savefig(dest)
