import os

from collections import namedtuple
from operator import attrgetter

try:
    import termcolor
except ImportError:
    termcolor = None  # noqa

try:
    import colorama
    TERMCOLOR2COLORAMA = {
        'green': colorama.Fore.GREEN,
        'yellow': colorama.Fore.YELLOW,
        'red': colorama.Fore.RED,
    }
except ImportError:
    colorama = None

# define constants
IS_NT = os.name == 'nt'

Result = namedtuple('Result', ['nodeid', 'result', 'duration'])


def _get_result_color(time_taken):
    """Get time taken result color."""
    time_taken_ms = time_taken * 1000
    if time_taken_ms <= 1000:
        color = 'green'
    elif time_taken_ms <= 3000:
        color = 'yellow'
    else:
        color = 'red'

    return color


def _colored_time(time_taken, timer_no_color=False):
    """Get formatted and colored string for a given time taken."""
    color = _get_result_color(time_taken)
    val = "{0:0.4f}s".format(time_taken)
    if timer_no_color:
        return val

    if termcolor is not None:
        val = termcolor.colored(val, color)
    elif colorama is not None:
        val = TERMCOLOR2COLORAMA[color] + val + colorama.Style.RESET_ALL
    return val


def pytest_addoption(parser):
    # Windows + nosetests does not support colors (even with colorama).
    if not IS_NT:
        group = parser.getgroup("terminal reporting", "reporting", after="general")
        group.addoption(
            "--timer-no-color",
            action="store_true",
            default=False,
            help="Don't colorize output (useful for non-tty output).",
        )

        group.addoption(
            "--timer-top-n",
            action="store",
            default=0,
            type=int,
            dest="timer_top_n",
            help="Show N slowest tests only. The default, -1, shows all tests.",
        )


def pytest_terminal_summary(terminalreporter):
    tr = terminalreporter
    results = []
    for reports in tr.stats.values():
        for rep in (r for r in reports if r.when == 'call'):
            if hasattr(rep, 'duration'):
                results.append(
                    Result(
                        nodeid=rep.nodeid,
                        result='success' if rep.passed else 'fail',
                        duration=rep.duration,
                    )
                )

    tr.write_sep('=', 'pytest-timer')
    result = list(sorted(results, key=attrgetter('duration'), reverse=True))
    timer_top_n = tr.config.option.timer_top_n
    if timer_top_n:
        result = result[:timer_top_n]

    for result in result:
        duration = _colored_time(
            time_taken=result.duration,
            timer_no_color=tr.config.option.timer_no_color,
        )
        tr.write_line("[{result}] {nodeid}: {duration}".format(
            result=result.result,
            nodeid=result.nodeid,
            duration=duration,
        ))
