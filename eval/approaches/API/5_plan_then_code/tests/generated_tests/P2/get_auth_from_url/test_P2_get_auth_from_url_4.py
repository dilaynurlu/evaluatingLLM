from requests.utils import get_auth_from_url

def test_get_auth_empty_password():
    """
    Test extraction when the password field is empty but the delimiter is present.
    URL format: http://user:@host
    """
    url = "http://myuser:@example.com"
    expected_auth = ("myuser", "")
    
    assert get_auth_from_url(url) == expected_auth