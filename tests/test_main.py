from click.testing import CliRunner
from unittest.mock import patch

from src.main import run
from src import main


@patch.object(main.Copyist, "__init__")
@patch.object(main.Copyist, "match_source_and_replica")
@patch.object(main, "configure_logging")
def test_run_function(mock_logging, mock_match, mock_instance):
    mock_instance.return_value = None
    runner = CliRunner()
    mock_match.side_effect = Exception
    result = runner.invoke(run, ['--catalog-source', 'catalog_source',
                                 '--catalog-replica', 'catalog_replica',
                                 '--period', '1',
                                 '--path-log', 'path_to_log']
                           )
    assert result.exit_code == 1
    mock_logging.assert_called_once_with('path_to_log')
    mock_instance.assert_called_once_with(
        'catalog_source', 'catalog_replica', mock_logging()
    )
    mock_match.assert_called_once()
