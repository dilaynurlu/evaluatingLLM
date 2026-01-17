import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_handles_empty_username_with_colon():
    """
    Test that if a colon is present but the username component is empty,
    an empty string is returned for the username.
    """
    url = "http://:secret@example.com"
    expected_auth = ("", "secret")
    
    assert get_auth_from_url(url) == expected_auth