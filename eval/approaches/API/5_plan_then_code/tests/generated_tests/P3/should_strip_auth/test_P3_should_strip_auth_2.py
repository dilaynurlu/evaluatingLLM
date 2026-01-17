import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com/resource", "https://example.com/resource"),
    ("http://example.com:80/resource", "https://example.com/resource"),
    ("http://example.com/resource", "https://example.com:443/resource"),
    ("http://example.com:80/resource", "https://example.com:443/resource"),
    ("http://exämple.com/resource", "https://exämple.com/resource"),
])
def test_should_strip_auth_secure_upgrades(old_url, new_url):
    """
    Test that authentication is preserved when upgrading from HTTP to HTTPS 
    on standard ports (80/443), including handling of explicit vs implicit ports.
    """
    session = Session()
    # Upgrading to HTTPS on the same host with standard ports is the only exception 
    # where scheme change is allowed without stripping auth.
    assert session.should_strip_auth(old_url, new_url) is False