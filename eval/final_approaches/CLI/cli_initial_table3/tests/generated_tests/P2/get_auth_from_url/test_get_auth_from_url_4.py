from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_auth():
    """
    Test extraction from URL with no auth.
    """
    url = "http://example.com/foo"
    auth = get_auth_from_url(url)
    
    # Should return empty auth.
    # The implementation catches exception and returns ("", "").
    # Wait, parsed.username is None. unquote(None) raises.
    # So it returns ("", "").
    
    assert auth == ("", "")
