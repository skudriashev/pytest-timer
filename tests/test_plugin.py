from parameterized import parameterized

from pytest_timer.plugin import (
    _colored_time,
    _get_result_color,
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
        (1.000, False, '\x1b[32m1.0000s\x1b[0m'),
        (1.001, False, '\x1b[33m1.0010s\x1b[0m'),
        (3.000, False, '\x1b[33m3.0000s\x1b[0m'),
        (3.001, False, '\x1b[31m3.0010s\x1b[0m'),
        (3.001, True, '3.0010s'),
    ])
    def test_colored_time(self, time_taken, timer_no_color, expected_result):
        assert _colored_time(time_taken, timer_no_color) == expected_result
