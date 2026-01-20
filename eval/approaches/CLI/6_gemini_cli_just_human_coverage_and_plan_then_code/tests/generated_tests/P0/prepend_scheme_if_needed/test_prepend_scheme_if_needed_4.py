
import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_just_path():
    # If it looks like a path but could be a host
    url = "foo/bar"
    # urlparse("foo/bar") -> scheme='', netloc='', path='foo/bar'
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://foo/bar"
