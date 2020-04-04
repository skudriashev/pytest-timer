from _pytest.config.argparsing import Parser
from parameterized import parameterized

from pytest_timer.plugin import (
    _colored_time,
    _get_result_color,
    pytest_addoption,
)


class TestPlugin:
    @parameterized.expand([
        (1.000, 'green'),
        (1.001, 'yellow'),
        (3.000, 'yellow'),
        (3.001, 'red'),
    ])
    def test_get_result_color(self, time_taken, color):
        assert _get_result_color(time_taken) == color

    @parameterized.expand([
        ('green', 1.000, False, '\x1b[32m1.0000s\x1b[0m'),
        ('yellow', 1.001, False, '\x1b[33m1.0010s\x1b[0m'),
        ('yellow', 3.000, False, '\x1b[33m3.0000s\x1b[0m'),
        ('red', 3.001, False, '\x1b[31m3.0010s\x1b[0m'),
        ('red', 3.001, True, '3.0010s'),
    ])
    def test_colored_time(self, color, time_taken, timer_no_color, expected_result):
        import time
        time.sleep(1)
        assert _colored_time(color, time_taken, timer_no_color) == expected_result

    def test_pytest_addoption(self):
        parser = Parser()

        pytest_addoption(parser)

        options = parser.getgroup("terminal reporting").options
        assert options[0].names() == ['--timer-top-n']
        assert options[1].names() == ['--timer-no-color']
        assert options[2].names() == ['--timer-filter']
