"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import date
import pytest

class InvalidDateString(Exception):
    pass


def calculate_days(date_str: str) -> int:
    try:
        from_date = date.fromisoformat(date_str)
    except ValueError:
        raise InvalidDateString
    return (date.today() - from_date).days


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""



def test_calculate_days(freezer):
    freezer.move_to('2025-03-25')
    assert calculate_days('2025-03-20') == 5
    assert calculate_days('2025-03-30') == -5


def test_calculate_days_invalid_format():
    with pytest.raises(InvalidDateString):
        calculate_days('2025-03-40')
        
    with pytest.raises(InvalidDateString):
        calculate_days('9999999999-03-01')
    
