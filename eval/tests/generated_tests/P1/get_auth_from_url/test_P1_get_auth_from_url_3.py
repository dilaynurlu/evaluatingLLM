from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password():
    """
    Test extraction when password is empty but colon is present.
    """
    url = "ftp://myuser:@example.com"
    expected_auth = ("myuser", "")
    
    assert get_auth_from_url(url) == expected_auth