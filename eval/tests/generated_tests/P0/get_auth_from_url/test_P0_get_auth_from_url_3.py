import pytest
from requests.utils import get_auth_from_url

def test_get_auth_no_credentials():
    """
    Test that a URL with no authentication components returns a tuple of empty strings.
    """
    url = "http://example.com/index.html"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth