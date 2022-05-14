import numpy as np
from matplotlib import pyplot as plt

from astro_tablets.constants import Precision
from astro_tablets.query.lunar_six_query import LunarSixQuery


def plot_lunar_six_score(expected_us: float, dest: str):

    xs = np.arange(expected_us - 20, expected_us + 20, 0.0001)
    f, ax1 = plt.subplots()
    ax1.set_xlabel("Time (UŠ)")
    ax1.set_ylabel("Score")

    ys = list(
        map(
            lambda x: LunarSixQuery.calculate_score(
                actual_us=x,
                tablet_us=expected_us,
                time_precision=Precision.REGULAR,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Regular Precision", color="b")

    ys = list(
        map(
            lambda x: LunarSixQuery.calculate_score(
                actual_us=x,
                tablet_us=expected_us,
                time_precision=Precision.LOW,
            ),
            xs,
        )
    )
    ax1.plot(xs, ys, label="Low Precision", color="g")

    ax1.axvline(x=expected_us, color="r", label="Expected Time")
    ax1.legend()
    plt.savefig(dest)
