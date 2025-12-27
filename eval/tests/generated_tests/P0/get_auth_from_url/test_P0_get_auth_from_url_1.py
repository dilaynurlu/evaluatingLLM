import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_valid_credentials():
    """
    Test extraction of plain text username and password from a URL.
    Verifies the standard success path.
    """
    url = "http://myuser:mypassword@example.com/resource"
    expected_auth = ("myuser", "mypassword")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth