import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that a URL with no authentication components returns a tuple of empty strings.
    """
    url = "http://www.example.com/index.html?query=param"
    expected_auth = ("", "")
    
    result = get_auth_from_url(url)
    
    assert result == expected_auth