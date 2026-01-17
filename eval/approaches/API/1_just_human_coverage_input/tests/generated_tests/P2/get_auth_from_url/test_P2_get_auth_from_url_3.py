from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test that a URL with no authentication information returns a tuple of empty strings.
    """
    url = "http://example.com/index.html"
    
    # When no auth is present, the function handles the missing attributes/types
    # and returns ("","")
    assert get_auth_from_url(url) == ("", "")