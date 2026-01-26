from requests.utils import get_auth_from_url

def test_get_auth_from_url_ipv6():
    """
    Test URL with IPv6 address literals (brackets) and auth.
    
    Verifies that the parsing logic correctly identifies the authority section
    when IPv6 brackets are present, preventing confusion between the address
    and the credentials.
    """
    url = "http://test_usr:test_secret_val@[::1]:8080/path"
    result = get_auth_from_url(url)
    assert result == ("test_usr", "test_secret_val")