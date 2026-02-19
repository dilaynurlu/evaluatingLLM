from requests.utils import get_auth_from_url

def test_get_auth_from_url_no_credentials():
    """
    Test URL (FTP scheme) with no authentication components.
    
    In this scenario, `urlparse` returns None for username/password.
    The function attempts `unquote(None)`, which raises a TypeError/AttributeError.
    The exception block catches this and returns ("", "").
    """
    url = "ftp://example.com/resource"
    result = get_auth_from_url(url)
    assert result == ("", "")