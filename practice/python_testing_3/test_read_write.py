"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import uuid
import string
from ..python_part_2.task_read_write import extract_numbers_from_files


def mock_and_run(nums: list[str], tmp_path) -> str:
    '''Creates mock files from the list of numbers, writing each element in a temp file,
    then runs the function and returns the contents of the results file.
    '''
    filenames = [str(uuid.uuid4()) + ".txt" for _ in nums]

    for filename, content in zip(filenames, nums):
        file_path = tmp_path / filename
        with open(file_path, 'w') as f:
            f.write(content)

    result_file = tmp_path / "result.txt"
    extract_numbers_from_files(tmp_path, result_file)

    with open(result_file, 'r') as f:
        result_content = f.read()

    return result_content


def test_extract_numbers_from_files(tmp_path):
    contents = ["23", "78", "3"]
    result_content = mock_and_run(contents, tmp_path)

    # The files might have been read in a different order,
    # So we'll check that the numbers are the same instead
    result_numbers = result_content.split(', ')
    
    assert len(result_numbers) == len(contents)
    assert all(n in contents for n in result_numbers)
