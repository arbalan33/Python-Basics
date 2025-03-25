"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math

import pytest


class OperationNotFoundException(Exception):
    pass


def math_calculate(function_name: str, *args):
    if len(args) not in (1, 2):
        raise ValueError
    
    try:
        func = getattr(math, function_name)
    except AttributeError:
        raise OperationNotFoundException

    return func(*args)
        


"""
Write tests for math_calculate function
"""

def test_math_calculate():
    assert math_calculate("log", 10) == math.log(10)
    assert math_calculate("pow", 10, 10) == math.pow(10, 10)


def test_math_calculate_nonexistent():
    with pytest.raises(OperationNotFoundException):
        math_calculate("foobar", 1)


def test_math_calculate_args_number():
    '''We're expecting a certain number of args'''
    with pytest.raises(ValueError):
        math_calculate("pi")
