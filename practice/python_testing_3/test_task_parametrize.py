"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""

import pytest

def fibonacci_1(n: int) -> int:
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return b


def fibonacci_2(n: int) -> int:
    fibo = [0, 1]
    for i in range(1, n+1):
        fibo.append(fibo[i-1] + fibo[i-2])
    return fibo[n]


def fibonacci_2_fixed(n: int) -> int:
    fibo = [0, 1]
    for i in range(1, n+1):
        fibo.append(fibo[i] + fibo[i-1])
    return fibo[n]



@pytest.mark.parametrize("fib", [fibonacci_1, 
                                #  fibonacci_2,
                                 fibonacci_2_fixed])
@pytest.mark.parametrize("inp,expected", [(1, 1), (10, 55)])
def test_fibbonacci(fib, inp, expected):
    assert fib(inp) == expected