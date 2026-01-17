from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password():
    """
    Test extraction when password is an empty string (indicated by a colon with no following characters).
    """
    url = "ftp://username:@ftp.example.com"
    expected_auth = ("username", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth