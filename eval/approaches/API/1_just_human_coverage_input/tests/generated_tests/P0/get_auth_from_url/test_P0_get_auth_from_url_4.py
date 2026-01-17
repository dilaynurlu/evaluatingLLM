import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_user_only_no_colon():
    """
    Test behavior when URL contains a username but no password and no colon.
    The implementation expects both components to be present/valid; otherwise,
    it catches the resulting TypeError (from unquote(None)) and returns empty auth.
    """
    url = "http://myuser@example.com"
    # Logic: parsed.password is None -> unquote(None) raises TypeError -> returns ("", "")
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth