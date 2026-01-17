from requests.utils import get_auth_from_url

def test_get_auth_missing_password_returns_empty():
    """
    Test that providing a username without a password delimiter (colon) results in
    empty extraction. This covers the internal TypeError handling path when 
    parsed.password is None.
    """
    # When no colon is present, urlparse sets password to None.
    # The function attempts unquote(None), catches TypeError, and returns ("", "").
    url = "http://useronly@example.com"
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth