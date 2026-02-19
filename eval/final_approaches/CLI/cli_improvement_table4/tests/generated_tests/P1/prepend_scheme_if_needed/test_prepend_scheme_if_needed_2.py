import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_has_scheme():
    """Test that existing scheme is preserved."""
    url = "https://example.com/path"
    result = prepend_scheme_if_needed(url, "http")
    assert result == "https://example.com/path"
