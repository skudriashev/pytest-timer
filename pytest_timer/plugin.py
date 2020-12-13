import os

from collections import namedtuple
from operator import attrgetter

try:
    import termcolor
except ImportError:  # pragma: no cover
    termcolor = None  # pragma: no cover

try:
    import colorama

    TERMCOLOR2COLORAMA = {
        "green": colorama.Fore.GREEN,
        "yellow": colorama.Fore.YELLOW,
        "red": colorama.Fore.RED,
    }
except ImportError:  # pragma: no cover
    colorama = None  # pragma: no cover

# define constants
IS_NT = os.name == "nt"

Result = namedtuple("Result", ["nodeid", "result", "color", "duration"])


def _get_result_color(time_taken):
    """Get time taken result color."""
    time_taken_ms = time_taken * 1000
    if time_taken_ms <= 1000:
        color = "green"
    elif time_taken_ms <= 3000:
        color = "yellow"
    else:
        color = "red"

    return color


def _colored_time(color, time_taken, timer_no_color=False):
    """Get formatted and colored string for a given time taken."""
    val = "{0:0.4f}s".format(time_taken)
    if timer_no_color:
        return val

    if termcolor is not None:
        val = termcolor.colored(val, color)
    elif colorama is not None:
        val = TERMCOLOR2COLORAMA[color] + val + colorama.Style.RESET_ALL
    return val


def pytest_addoption(parser):
    group = parser.getgroup("terminal reporting", "reporting", after="general")

    group.addoption(
        "--timer-top-n",
        action="store",
        default=0,
        type=int,
        dest="timer_top_n",
        help="Show N slowest tests only. The default, -1, shows all tests.",
    )

    # Windows + nosetests does not support colors (even with colorama).
    if not IS_NT:
        group.addoption(
            "--timer-no-color",
            action="store_true",
            default=False,
            help="Don't colorize output (useful for non-tty output).",
        )

    group.addoption(
        "--timer-filter",
        action="store",
        default=None,
        dest="timer_filter",
        help="Show filtered results only (ok,warning,error).",
    )


def pytest_terminal_summary(terminalreporter):
    tr = terminalreporter
    tr.write_sep("=", "pytest-timer")

    timer_filter = (
        tr.config.option.timer_filter.split(",")
        if tr.config.option.timer_filter is not None
        else None
    )
    timer_top_n = tr.config.option.timer_top_n

    results = []
    total_time = 0
    for report_type, reports in tr.stats.items():
        # no need to report deselected tests (-k EXPRESSION)
        if report_type == "deselected":
            continue
        for rep in (r for r in reports if r.when == "call"):
            if hasattr(rep, "duration"):
                duration = rep.duration
                color = _get_result_color(time_taken=duration)
                results.append(
                    Result(
                        nodeid=rep.nodeid,
                        result="success" if rep.passed else "fail",
                        color=color,
                        duration=duration,
                    )
                )
                total_time += rep.duration

    shown = 0
    for result in list(sorted(results, key=attrgetter("duration"), reverse=True)):
        if timer_top_n and shown >= timer_top_n:
            break

        if timer_filter is not None:
            filter_name = {"green": "ok", "yellow": "warning", "red": "error"}.get(
                result.color
            )
            if timer_filter is not None and filter_name not in timer_filter:
                continue

        duration = _colored_time(
            color=result.color,
            time_taken=result.duration,
            timer_no_color=tr.config.option.timer_no_color,
        )
        percent = 0 if total_time == 0 else result.duration / total_time * 100
        tr.write_line(
            "[{result}] {percent:04.2f}% {nodeid}: {duration}".format(
                result=result.result,
                percent=percent,
                nodeid=result.nodeid,
                duration=duration,
            )
        )
        shown += 1
