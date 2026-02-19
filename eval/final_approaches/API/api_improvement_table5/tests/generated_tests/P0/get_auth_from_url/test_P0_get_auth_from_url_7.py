import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_with_ipv6_host():
    """
    Test extracting credentials from a URL with an IPv6 literal host.
    Ensures parsing logic holds up with complex netlocs.
    """
    url = "http://ipv6user:ipv6pass@[2001:db8::1]/"
    auth = get_auth_from_url(url)
    
    assert auth == ("ipv6user", "ipv6pass")