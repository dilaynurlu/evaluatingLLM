from requests.utils import get_auth_from_url

def test_get_auth_from_url_empty_password_with_port():
    """
    Test extraction where the username is present but the password is an empty string,
    within a URL that includes a port number.
    Syntax: ftp://user:@host:port
    
    Refines coverage for:
    - Missing URL Component Variations (Port integration with edge-case auth).
    """
    url = "ftp://user:@example.com:21/resource"
    auth = get_auth_from_url(url)
    
    assert auth == ("user", "")