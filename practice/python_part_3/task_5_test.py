"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from unittest.mock import Mock, patch, MagicMock
import pytest
from typing import Tuple


import urllib.request


def make_request(url: str) -> Tuple[int, str]:
    with urllib.request.urlopen(url) as response:
        status_code = response.getcode()  # Get HTTP status code
        data = response.read().decode('utf-8')  # Read and decode response
        return status_code, data


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""


def test_make_request_success():
    '''urlopen returns a context manager, so we need to patch that.'''
    cm = MagicMock()
    cm.getcode.return_value = 200
    cm.read.return_value = b'Fake response text'
    cm.__enter__.return_value = cm
    mock_urlopen = Mock()
    mock_urlopen.return_value = cm

    with patch('urllib.request.urlopen', return_value=cm):
        status, content = make_request('https://example.com')

    assert status == 200
    assert content == 'Fake response text'