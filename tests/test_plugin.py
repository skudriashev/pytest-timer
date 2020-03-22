from pytest_timer.plugin import _get_result_color


class TestPlugin:
    def test_get_result_color_green(self):
        assert _get_result_color(1.000) == 'green'

    def test_get_result_color_yellow(self):
        assert _get_result_color(3.000) == 'yellow'

    def test_get_result_color_red(self):
        assert _get_result_color(3.001) == 'red'
