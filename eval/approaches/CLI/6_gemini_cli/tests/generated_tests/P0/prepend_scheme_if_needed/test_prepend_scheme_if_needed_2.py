
import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_with_scheme():
    url = "https://example.com"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "https://example.com"
