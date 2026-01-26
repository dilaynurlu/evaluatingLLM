from requests.utils import get_auth_from_url

def test_get_auth_from_url_partial_credentials_user_only():
    """
    Test URL with username only (no colon delimiter).
    
    Standard `urlparse` behavior sets `password` to None in this case.
    The implementation attempts `unquote(None)` for the password, which fails.
    Consequently, the function catches the exception and returns ("", "").
    This test verifies that the fallback logic suppresses the partial credential.
    """
    url = "http://test_usr@example.com"
    result = get_auth_from_url(url)
    assert result == ("", "")