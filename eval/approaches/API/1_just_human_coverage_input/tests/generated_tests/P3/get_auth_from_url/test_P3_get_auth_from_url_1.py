import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic_credentials():
    """
    Test extraction of standard plain text username and password.
    Verifies the happy path for HTTP URLs.
    """
    url = "http://username:password@example.com/resource"
    expected_auth = ("username", "password")
    
    assert get_auth_from_url(url) == expected_auth