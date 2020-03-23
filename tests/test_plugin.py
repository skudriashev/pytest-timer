from parameterized import parameterized

from pytest_timer.plugin import _get_result_color


class TestPlugin:
    @parameterized.expand([
        (1.000, 'green'),
        (1.001, 'yellow'),
        (3.000, 'yellow'),
        (3.001, 'red'),
    ])
    def test_get_result_color(self, time_taken, color):
        assert _get_result_color(time_taken) == color

    def test_colored_time(self):
        pass
