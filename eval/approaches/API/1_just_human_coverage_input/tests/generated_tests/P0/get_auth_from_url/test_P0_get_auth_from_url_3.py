import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password_with_colon():
    """
    Test extraction when the password is explicitly empty (indicated by a colon).
    """
    url = "http://myuser:@example.com"
    expected_auth = ("myuser", "")
    
    assert get_auth_from_url(url) == expected_auth