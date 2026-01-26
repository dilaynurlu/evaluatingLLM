import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_upgrade_standard_ports():
    """
    Test that Authorization header is KEPT when upgrading from HTTP to HTTPS
    on standard ports (80/443 or implicit).
    Matches special case: http -> https with ports in (80/443, None).
    """
    session = Session()
    # Implicit ports (http=80, https=443)
    old_url = "http://example.com/login"
    new_url = "https://example.com/login"
    
    # Upgrade to secure scheme on same host -> should NOT strip auth
    assert session.should_strip_auth(old_url, new_url) is False