import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_double_slash():
    url = "//google.com"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://google.com"
