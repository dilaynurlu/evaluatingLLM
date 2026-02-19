import pytest
from requests.utils import prepend_scheme_if_needed

def test_prepend_scheme_if_needed_just_host():
    """Test prepending scheme to just a hostname."""
    url = "example.com"
    result = prepend_scheme_if_needed(url, "https")
    assert result == "https://example.com"
