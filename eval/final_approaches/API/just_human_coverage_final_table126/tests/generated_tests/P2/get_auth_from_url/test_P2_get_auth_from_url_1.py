import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic_credentials():
    """
    Test extraction of simple, unencoded username and password 
    from a standard URL.
    """
    url = "http://username:password@example.com/resource"
    expected_auth = ("username", "password")
    
    assert get_auth_from_url(url) == expected_auth