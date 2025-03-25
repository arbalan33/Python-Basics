"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""
import re
import pytest


URL_REGEX = re.compile(r"^https?:\/\/[^\s\/$.?#].[^\s]*$")

def is_http_url(url: str) -> bool:
    return bool(URL_REGEX.match(url))


@pytest.mark.parametrize("url, is_valid", [
    ("http://example.com", True),
    ("https://example.com", True),
    ("http://example.com/path?query=value", True),
    ("https://sub.domain.com:8080/path#anchor", True),
    ("ftp://example.com", False),  # Wrong protocol
    ("example.com", False),  # Missing http(s)
    ("http:/example.com", False),  # a single slash
    ("http:/example.com/ test", False),  # whitespace after domain
    ("http://", False),  # Incomplete URL
    ("http://exa mple.com", False),  # Space in URL
])
def test_is_http_url(url, is_valid):
    assert is_http_url(url) == is_valid
