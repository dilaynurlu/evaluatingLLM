import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_partial_auth_user_only():
    """
    Test that a URL with only a username (no password, no colon) results in empty auth.
    
    When urlparse parses 'http://user@host', password is None.
    The function attempts unquote(None), which raises TypeError, caught by the except block.
    """
    url = "http://justuser@example.com"
    expected_auth = ("", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth