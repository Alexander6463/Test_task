from unittest.mock import patch

from src import log
from src.log import configure_logging


@patch.object(log.logging, "FileHandler")
@patch.object(log, "Path")
def test_create_log_file(mock_filehandler, mock_path):
    configure_logging("some_path/file.log")
    mock_path.assert_called_once_with("some_path/file.log")
    mock_filehandler.assert_called_once_with("some_path/file.log")
