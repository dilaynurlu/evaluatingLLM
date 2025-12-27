import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_missing_password_component():
    """
    Test behavior when the password component is completely missing (no colon).
    urlparse sets password to None in this case, which causes unquote to raise TypeError.
    The function should catch this and return empty auth.
    """
    # Note: 'http://user@host' implies username='user', password=None.
    # Because one of the components (password) is None, unquote fails, and the function falls back to ("", "").
    url = "http://lonelyuser@example.com"
    expected_auth = ("", "")
    
    result = get_auth_from_url(url)
    
    assert result == expected_auth