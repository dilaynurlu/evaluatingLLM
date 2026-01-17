import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_returns_empty_tuple_for_username_only_no_colon():
    """
    Test that a URL with a username but no colon/password returns empty strings.
    
    In this scenario, urlparse returns a username but None for password.
    The internal unquote function raises TypeError on None, which is caught 
    by get_auth_from_url, resulting in ("", "").
    """
    url = "http://user@example.com"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth