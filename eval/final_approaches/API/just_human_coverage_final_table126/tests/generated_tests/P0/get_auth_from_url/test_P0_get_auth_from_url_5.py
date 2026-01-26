import pytest
from requests.utils import get_auth_from_url

def test_get_auth_empty_username_field():
    """
    Test extracting auth when the username field is empty.
    Format: http://:password@host
    """
    url = "https://:secret123@api.example.org"
    expected_auth = ("", "secret123")
    
    assert get_auth_from_url(url) == expected_auth