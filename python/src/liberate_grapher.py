from typing import Sequence, Tuple
import logging
from logging import info, debug

import matplotlib.pyplot as plt  # type: ignore

from src.liberty_parser import LibertyResult
from src.utils import single


def graph_cell_delay(
    ldb: LibertyResult,
    pin: str,
    delay_index: Tuple[int, int],
    x_axis: Sequence[float],
    x_axis_title: str,
    out_path: str,
) -> None:

    di1, di2 = delay_index
    # pylint: disable=no-member
    rise_times = [
        single(lambda p: p.name == pin, cell.pin)
        .timing[0]
        .cell_rise[0]
        .values[di1][di2]
        for cell in ldb.cell  # type: ignore
    ]
    fall_times = [
        single(lambda p: p.name == pin, cell.pin)
        .timing[0]
        .cell_fall[0]
        .values[di1][di2]
        for cell in ldb.cell  # type: ignore
    ]

    assert len({len(rise_times), len(fall_times), len(x_axis)}) == 1

    info("Generating graph of results.")

    mpl_logger = logging.getLogger("matplotlib")
    if logging.getLogger().getEffectiveLevel() < logging.WARNING:
        debug("Suppressing matplotlib logs below warning.")
        mpl_logger.setLevel(logging.WARNING)

    plt.figure()
    plt.title(f"{x_axis_title} vs Rise and Fall time")
    plt.plot(x_axis, rise_times, "b")
    plt.plot(x_axis, fall_times, "g")
    plt.legend(["cell rise", "cell fall"])
    plt.ylabel("Delay")
    plt.xlabel(x_axis_title)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which="major", linestyle="-", linewidth="0.5", color="red")
    ax.grid(which="minor", linestyle=":", linewidth="0.5", color="black")
    plt.savefig(out_path)
