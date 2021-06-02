import warnings
from unittest import mock

from _pytest.config.argparsing import Parser
from parameterized import parameterized
from pytest import fixture

from pytest_timer import plugin


@fixture
def tr_mock(mocker):
    tr_mock = mocker.Mock()
    tr_mock.config.option.timer_top_n = None
    tr_mock.config.option.timer_filter = None
    tr_mock.stats = {
        "passed": [
            mocker.Mock(when="call", nodeid="1", duration=3.01),
            mocker.Mock(when="call", nodeid="2", duration=1.01),
            mocker.Mock(when="call", nodeid="3", duration=0.99),
        ],
        "deselected": [
            mocker.Mock(when="call", nodeid="4", duration=1.00),
        ],
    }
    return tr_mock


class TestPlugin:
    @parameterized.expand(
        [(1.000, "green"), (1.001, "yellow"), (3.000, "yellow"), (3.001, "red")]
    )
    def test_get_result_color(self, time_taken, color):
        assert plugin._get_result_color(time_taken) == color

    @parameterized.expand(
        [
            ("green", 1.000, False, "\x1b[32m1.0000s\x1b[0m"),
            ("yellow", 1.001, False, "\x1b[33m1.0010s\x1b[0m"),
            ("yellow", 3.000, False, "\x1b[33m3.0000s\x1b[0m"),
            ("red", 3.001, False, "\x1b[31m3.0010s\x1b[0m"),
            ("red", 3.001, True, "3.0010s"),
        ]
    )
    def test_colored_time(self, color, time_taken, timer_no_color, expected_result):
        assert (
            plugin._colored_time(color, time_taken, timer_no_color) == expected_result
        )

    @parameterized.expand(
        [
            ("green", 1.000, False, "\x1b[32m1.0000s\x1b[0m"),
            ("yellow", 1.001, False, "\x1b[33m1.0010s\x1b[0m"),
            ("yellow", 3.000, False, "\x1b[33m3.0000s\x1b[0m"),
            ("red", 3.001, False, "\x1b[31m3.0010s\x1b[0m"),
            ("red", 3.001, True, "3.0010s"),
        ]
    )
    def test_colored_time_colorama(
        self, color, time_taken, timer_no_color, expected_result
    ):
        with mock.patch.object(plugin, "termcolor", None):
            assert (
                plugin._colored_time(color, time_taken, timer_no_color)
                == expected_result
            )

    def test_pytest_addoption(self):
        parser = Parser()

        plugin.pytest_addoption(parser)

        options = parser.getgroup("terminal reporting").options
        assert options[0].names() == ["--timer-top-n"]
        assert options[1].names() == ["--timer-no-color"]
        assert options[2].names() == ["--timer-filter"]

    def test_pytest_terminal_summary(self, mocker, tr_mock):
        plugin.pytest_terminal_summary(terminalreporter=tr_mock)

        tr_mock.write_line.assert_has_calls(
            [
                mocker.call("[success] 60.08% 1: 3.0100s"),
                mocker.call("[success] 20.16% 2: 1.0100s"),
                mocker.call("[success] 19.76% 3: 0.9900s"),
            ]
        )

    def test_pytest_terminal_summary_with_timer_top_n(self, mocker, tr_mock):
        tr_mock.config.option.timer_top_n = 1

        plugin.pytest_terminal_summary(terminalreporter=tr_mock)

        tr_mock.write_line.assert_has_calls(
            [mocker.call("[success] 60.08% 1: 3.0100s")]
        )

    def test_pytest_terminal_summary_with_timer_filter_error(self, mocker, tr_mock):
        tr_mock.config.option.timer_filter = "error"

        plugin.pytest_terminal_summary(terminalreporter=tr_mock)

        tr_mock.write_line.assert_has_calls(
            [mocker.call("[success] 60.08% 1: 3.0100s")]
        )

    def test_pytest_terminal_summary_with_timer_filter_warning(self, mocker, tr_mock):
        tr_mock.config.option.timer_filter = "warning"

        plugin.pytest_terminal_summary(terminalreporter=tr_mock)

        tr_mock.write_line.assert_has_calls(
            [mocker.call("[success] 20.16% 2: 1.0100s")]
        )

    def test_pytest_terminal_summary_with_timer_filter_error_warning(
        self, mocker, tr_mock
    ):
        tr_mock.config.option.timer_filter = "error,warning"

        plugin.pytest_terminal_summary(terminalreporter=tr_mock)

        tr_mock.write_line.assert_has_calls(
            [
                mocker.call("[success] 60.08% 1: 3.0100s"),
                mocker.call("[success] 20.16% 2: 1.0100s"),
            ]
        )

    def test_pytest_terminal_summary_with_user_warning(self, mocker, tr_mock):
        warnings.warn("Test Warning to be used in tests")

        plugin.pytest_terminal_summary(terminalreporter=tr_mock)

        tr_mock.write_line.assert_has_calls(
            [
                mocker.call("[success] 60.08% 1: 3.0100s"),
                mocker.call("[success] 20.16% 2: 1.0100s"),
                mocker.call("[success] 19.76% 3: 0.9900s"),
            ]
        )
