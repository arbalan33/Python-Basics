"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import pytest
from ..python_part_2.task_read_write_2 import write_cp1252, write_utf8

@pytest.fixture
def sample_words():
    return ['abc', 'def', 'xyz']


def test_write_utf8(tmp_path, sample_words):
    utf8_file = tmp_path / "file1.txt"
    write_utf8(sample_words, utf8_file)
    
    with open(utf8_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert content == "abc\ndef\nxyz"


def test_write_cp1252(tmp_path, sample_words):
    cp1252_file = tmp_path / "file2.txt"
    write_cp1252(sample_words, cp1252_file)
    
    with open(cp1252_file, 'r', encoding='cp1252') as f:
        content = f.read()
    
    assert content == "xyz,def,abc"
