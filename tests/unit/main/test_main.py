import contextlib
import sys
from unittest.mock import patch

import pytest

from src.ytdl_sub.main import main
from ytdl_sub.utils.exceptions import ValidationException
from ytdl_sub.utils.logger import Logger


@pytest.fixture
def expected_uncaught_error_message():
    return (
        f"Please upload the error log file '%s' and make a "
        f"Github issue at https://github.com/jmbannon/ytdl-sub/issues with your config and "
        f"command/subscription yaml file to reproduce. Thanks for trying ytdl-sub!"
    )


@pytest.fixture
def mock_sys_exit():
    @contextlib.contextmanager
    def _mock_sys_exit(expected_exit_code: int):
        with patch.object(sys, "exit") as mock_exit:
            yield mock_exit

        assert mock_exit.called
        assert mock_exit.call_args_list[0].args[0] == expected_exit_code

    return _mock_sys_exit


def test_main_success(mock_sys_exit):
    with mock_sys_exit(expected_exit_code=0):
        with patch("src.ytdl_sub.main._main"):
            main()


def test_main_validation_error(capsys, mock_sys_exit):
    validation_exception = ValidationException("test")
    with mock_sys_exit(expected_exit_code=1):
        with patch("src.ytdl_sub.main._main", side_effect=validation_exception):
            with patch("src.ytdl_sub.main.logger") as mock_logger:
                main()

    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args.args[0] == validation_exception


def test_main_uncaught_error(capsys, mock_sys_exit, expected_uncaught_error_message):
    uncaught_error = ValueError("test")
    with mock_sys_exit(expected_exit_code=1):
        with patch("src.ytdl_sub.main._main", side_effect=uncaught_error):
            with patch("src.ytdl_sub.main.logger") as mock_logger:
                main()

    assert mock_logger.exception.call_count == 1
    assert mock_logger.exception.call_args.args[0] == "An uncaught error occurred:"

    assert mock_logger.error.call_count == 1
    assert mock_logger.error.call_args.args[0] == expected_uncaught_error_message
    assert mock_logger.error.call_args.args[1] == Logger.debug_log_filename()
