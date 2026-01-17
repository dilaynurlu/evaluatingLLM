
import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_https_default():
    url = "example.com"
    new_url = prepend_scheme_if_needed(url, "https")
    assert new_url == "https://example.com"
