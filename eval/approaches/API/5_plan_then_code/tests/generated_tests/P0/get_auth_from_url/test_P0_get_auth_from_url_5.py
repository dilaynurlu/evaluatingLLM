from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that a URL with no authentication components returns empty strings.
    """
    url = "http://www.google.com/search?q=test"
    expected_auth = ("", "")
    
    auth = get_auth_from_url(url)
    
    assert auth == expected_auth