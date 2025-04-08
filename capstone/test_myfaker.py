import pytest
import myfaker
from unittest.mock import patch
import uuid
from pathlib import Path

SCHEMA_FILE_CONTENTS = '''MOCKED'''


@pytest.fixture
def temp_json_schema_file(tmp_path):
    file_path = tmp_path / "schema.json"
    file_path.write_text(SCHEMA_FILE_CONTENTS)
    return file_path


def test_read_schema_from_json_file(temp_json_schema_file, capsys):
    '''Test that the CLI app reads the schema file, processes it and prints the result
    '''
    with patch('myfaker.generate_object') as mock_process:
        # mock the interpreter function to return its input
        mock_process.side_effect = lambda inp: inp

        myfaker.run_cli(["out", "-s", str(temp_json_schema_file)])
    captured = capsys.readouterr()
    assert captured.out == f'"{SCHEMA_FILE_CONTENTS}"\n'


@pytest.fixture
def temp_output_dir_with_files(tmp_path):
    file_path = tmp_path / "schema.json"
    file_path.write_text(SCHEMA_FILE_CONTENTS)
    return file_path


@pytest.fixture
def output_dir_with_diverse_files(tmp_path, prefix) -> tuple[Path, list]:
    '''Returns a tmppath with a directory called 'out' that contains 10 files:
    5 files start with the given prefix, while the other 5 have a random filename'''
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    files = []
    for i in range(10):
        if i < 5:
            filename = out_dir / f"{prefix}{uuid.uuid4().hex[:6]}.txt"
        else:
            filename = out_dir / f"{uuid.uuid4().hex[:10]}.txt"
        filename.write_text(f"Content for {filename.name}")
        files.append(filename)

    return tmp_path, out_dir


@pytest.mark.parametrize("files_count,expected_remaining_files", [
    # matching files (5) are removed, 5 remain, then one is written
    (1, 5+1),
    # no files are removed
    (0, 10)])
@pytest.mark.parametrize("prefix", ["test"])
def test_clear_path(output_dir_with_diverse_files, prefix, files_count, expected_remaining_files):
    '''Test that files with the same prefix are deleted from the output directory
    when --clear-path is specified, and files-count > 0, but not when files-count == 0'''
    tmp_path, out_dir = output_dir_with_diverse_files
    with patch('myfaker.generate_object') as mock_process:
        mock_process.return_value = 'MOCK'

        myfaker.run_cli([str(out_dir), "-s", '{}', '--file-name=test',
                        '--clear-path', '--files-count', str(files_count)])

    remaining_files = list(out_dir.iterdir())
    assert len(remaining_files) == expected_remaining_files


def test_saving_files(tmp_path):
    files_count = 13

    out_dir = tmp_path / 'out'
    out_dir.mkdir()

    with patch('myfaker.generate_object') as mock_process:
        mock_process.return_value = 'MOCK'
        myfaker.run_cli([str(out_dir), "-s", '{}',
                        '--file-name=test', '--files-count', str(files_count)])

    files = list(out_dir.iterdir())
    assert len(files) == files_count
    for f in files:
        assert f.read_text() == '"MOCK"\n'




def test_multiprocessing(tmp_path):
    '''More of an integration test because mocking multiprocessing is more involved'''
    files_count = 100

    out_dir = tmp_path / 'out'
    out_dir.mkdir()

    myfaker.run_cli([str(out_dir), "-s", '{"time": "timestamp:"}',
                    '--file-name=test', '--files-count', str(files_count),
                    '--multiprocessing', str(8)])

    files = list(out_dir.iterdir())
    assert len(files) == files_count
