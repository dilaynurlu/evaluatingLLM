import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_port_no_scheme():
    url = "example.com:8080"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://example.com:8080"
