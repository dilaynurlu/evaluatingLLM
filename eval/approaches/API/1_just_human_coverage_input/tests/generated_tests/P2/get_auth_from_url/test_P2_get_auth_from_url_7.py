from requests.utils import get_auth_from_url

def test_get_auth_from_url_ipv6_host():
    """
    Test extraction of credentials from a URL containing an IPv6 literal host.
    """
    # IPv6 hosts are enclosed in brackets; auth appears before the brackets.
    url = "http://myuser:mypass@[2001:db8::1]:8080/path"
    expected = ("myuser", "mypass")
    
    assert get_auth_from_url(url) == expected