import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_valid_credentials():
    """
    Test extracting a standard username and password from a URL.
    Should return the decoded username and password.
    """
    url = "http://user:password@example.com/path"
    auth = get_auth_from_url(url)
    
    assert isinstance(auth, tuple)
    assert len(auth) == 2
    assert auth == ("user", "password")