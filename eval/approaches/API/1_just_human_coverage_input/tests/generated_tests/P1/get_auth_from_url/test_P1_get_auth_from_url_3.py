import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_empty_password_with_colon():
    """
    Test that if a colon is present but the password component is empty,
    an empty string is returned for the password.
    """
    url = "http://admin:@example.com"
    expected_auth = ("admin", "")
    
    assert get_auth_from_url(url) == expected_auth