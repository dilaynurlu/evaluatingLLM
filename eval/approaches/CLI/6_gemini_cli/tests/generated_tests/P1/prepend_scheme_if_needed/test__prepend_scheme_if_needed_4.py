import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_ipv4():
    url = "127.0.0.1"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://127.0.0.1"