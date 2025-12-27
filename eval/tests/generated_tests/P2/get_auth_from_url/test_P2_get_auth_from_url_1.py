import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_basic_credentials():
    """
    Test extracting standard plaintext username and password from a URL.
    """
    url = "http://myuser:mypassword@example.com/resource"
    expected_auth = ("myuser", "mypassword")
    
    result = get_auth_from_url(url)
    
    assert result == expected_auth