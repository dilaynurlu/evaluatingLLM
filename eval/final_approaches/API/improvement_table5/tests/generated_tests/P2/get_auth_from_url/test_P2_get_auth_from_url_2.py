import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_valid_basic_credentials():
    """
    Test that standard username and password are correctly extracted from a URL.
    """
    url = "http://alice:secret123@example.com/resource"
    expected_auth = ("alice", "secret123")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth