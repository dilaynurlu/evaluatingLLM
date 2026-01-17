import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_query():
    url = "example.com?q=1"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://example.com?q=1"
