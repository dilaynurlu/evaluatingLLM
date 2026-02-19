import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password_field():
    """
    Test extraction when the password field is empty but the delimiter (colon) is present.
    Format: user:@host
    """
    url = "http://myuser:@example.org"
    # An empty password after the colon is valid and should result in an empty string.
    expected_auth = ("myuser", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth