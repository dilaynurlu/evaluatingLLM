import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_with_auth():
    """Test prepending scheme to URL with auth."""
    url = "//user:pass@example.com"
    result = prepend_scheme_if_needed(url, "http")
    assert result == "http://user:pass@example.com"
