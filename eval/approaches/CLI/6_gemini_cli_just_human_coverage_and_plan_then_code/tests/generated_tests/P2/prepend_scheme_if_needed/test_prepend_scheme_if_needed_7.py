import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_valid_scheme_chars():
    # Use standard scheme that urllib3 supports
    url = "ftp://example.com"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "ftp://example.com"
