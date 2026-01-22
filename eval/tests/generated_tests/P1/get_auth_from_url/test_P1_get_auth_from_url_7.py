from requests.utils import get_auth_from_url

def test_get_auth_from_url_missing_password_delimiter():
    """
    Test behavior when username is present but no colon/password is provided.
    In this case, urlparse sets password to None.
    The implementation attempts to unquote None, catches TypeError, and returns empty strings.
    """
    url = "http://user@example.com"
    # Even though 'user' is present, the failure to process 'None' password 
    # causes the entire auth extraction to fall back to empty strings.
    expected_auth = ("", "")
    
    assert get_auth_from_url(url) == expected_auth