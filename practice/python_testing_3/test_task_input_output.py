"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
import pytest
from io import StringIO
from unittest.mock import patch
from ..python_part_2.task_input_output import read_numbers


def test_average_numbers(capsys):
    with patch('sys.stdin', StringIO('1,2,hello,2,world\n')):
        result = read_numbers(5)
    assert result == "Avg: 1.67"


def test_no_numbers_entered(capsys):
    with patch('sys.stdin', StringIO('hello,world,foo,bar,baz\n')):
        result = read_numbers(5)
    assert result == "No numbers entered"


def test_partial_valid_numbers(capsys):
    with patch('sys.stdin', StringIO('10,abc,5,xyz,5\n')):
        result = read_numbers(5)
    assert result == "Avg: 6.67"


def test_all_valid_numbers(capsys):
    with patch('sys.stdin', StringIO('3,6,9\n')):
        result = read_numbers(3)
    assert result == "Avg: 6.0"


def test_extra_inputs_error(capsys):
    with patch('sys.stdin', StringIO('5,10,15\n')):
        with pytest.raises(RuntimeError) as excinfo:
            assert read_numbers(2) == "Avg: 15.0"
