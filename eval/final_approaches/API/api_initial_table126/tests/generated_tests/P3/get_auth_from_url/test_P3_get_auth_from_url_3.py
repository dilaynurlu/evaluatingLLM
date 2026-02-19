import pytest
from requests.utils import get_auth_from_url

def test_get_auth_no_credentials():
    """
    Test that a URL with no authentication components returns a tuple
    of empty strings.
    """
    url = "http://www.example.com/index.html"
    expected_auth = ("", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth