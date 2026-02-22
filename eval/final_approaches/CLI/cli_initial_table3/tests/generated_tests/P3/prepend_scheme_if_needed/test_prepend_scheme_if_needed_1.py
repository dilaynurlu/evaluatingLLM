import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_1():
    url = "example.com/path"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://example.com/path"
