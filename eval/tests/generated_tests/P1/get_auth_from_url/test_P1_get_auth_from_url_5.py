from requests.utils import get_auth_from_url

def test_get_auth_from_url_ipv6_host():
    """
    Test extraction of credentials when the host is an IPv6 literal.
    """
    url = "http://admin:secret@[2001:db8::1]:8080/status"
    expected_auth = ("admin", "secret")
    
    assert get_auth_from_url(url) == expected_auth