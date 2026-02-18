import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_no_scheme():
    """Test prepending scheme to a URL without one."""
    url = "example.com/path"
    result = prepend_scheme_if_needed(url, "http")
    assert result == "http://example.com/path"
