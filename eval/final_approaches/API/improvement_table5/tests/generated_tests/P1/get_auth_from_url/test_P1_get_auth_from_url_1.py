import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic_credentials():
    """
    Test that username and password are extracted correctly from a URL 
    containing standard plain-text credentials.
    """
    url = "http://myuser:mypassword@example.com/resource"
    expected_auth = ("myuser", "mypassword")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth