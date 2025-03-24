"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""
import pytest

from ..python_part_2.task_exceptions import *


def test_division_ok(capfd):
    res = division(4, 2)
    assert res == 2
    captured = capfd.readouterr()
    assert captured.out == "2\nDivision finished\n"


def test_division_by_zero(capfd):
    res = division(4, 0)
    assert res == None
    captured = capfd.readouterr()
    assert captured.out == "Division by 0\nDivision finished\n"


def test_division_by_one(capfd):
    with pytest.raises(DivisionByOneException) as excinfo:
        res = division(4, 1)
        assert res == None
        captured = capfd.readouterr()
        assert captured.out == "Division finished\n"
        assert "Division by 1 gives the same number" in str(excinfo.value)
