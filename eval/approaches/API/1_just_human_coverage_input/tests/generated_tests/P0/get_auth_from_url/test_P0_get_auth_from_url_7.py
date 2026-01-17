import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_ipv6_host():
    """
    Test extraction of credentials when the host is an IPv6 literal.
    """
    url = "http://ipv6user:ipv6pass@[::1]:8080/path"
    expected_auth = ("ipv6user", "ipv6pass")
    
    assert get_auth_from_url(url) == expected_auth