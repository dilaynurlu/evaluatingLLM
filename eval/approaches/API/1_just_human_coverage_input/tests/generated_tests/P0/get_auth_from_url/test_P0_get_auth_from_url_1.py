import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic_credentials():
    """
    Test extraction of standard plaintext username and password.
    """
    url = "http://user:password@example.com/resource"
    expected_auth = ("user", "password")
    
    assert get_auth_from_url(url) == expected_auth