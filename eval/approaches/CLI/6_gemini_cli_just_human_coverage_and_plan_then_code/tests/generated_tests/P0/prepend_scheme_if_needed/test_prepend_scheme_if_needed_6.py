
import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_double_slash():
    url = "//example.com"
    # urlparse("//example.com") -> scheme='', netloc='example.com'
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://example.com"
