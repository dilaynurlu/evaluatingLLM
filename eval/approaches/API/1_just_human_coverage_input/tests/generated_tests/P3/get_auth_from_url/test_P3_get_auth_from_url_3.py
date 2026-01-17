import pytest
from requests.utils import get_auth_from_url

def test_get_auth_from_url_ipv6_handling():
    """
    Test URL parsing with IPv6 literals.
    IPv6 addresses contain colons, which is also the separator for username:password.
    The parser must distinguish the credential separator from the IP address.
    """
    # Case 1: IPv6 with authentication
    url_auth = "http://user:password@[::1]:8080/resource"
    assert get_auth_from_url(url_auth) == ("user", "password")

    # Case 2: IPv6 without authentication (should not return auth components)
    # The colons in the IPv6 host should not be mistaken for credential separators.
    url_no_auth = "http://[::1]/index.html"
    assert get_auth_from_url(url_no_auth) == ("", "")