import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_path_only():
    url = "example.com/foo/bar"
    new_url = prepend_scheme_if_needed(url, "http")
    assert new_url == "http://example.com/foo/bar"
