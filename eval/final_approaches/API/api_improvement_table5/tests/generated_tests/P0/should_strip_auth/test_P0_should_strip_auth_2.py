import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_standard_ports():
    """
    Test that authentication is preserved (not stripped) when redirecting from HTTP to HTTPS
    on standard ports (80/443).
    """
    session = Session()
    # http (implicit port 80) -> https (implicit port 443)
    old_url = "http://example.com/login"
    new_url = "https://example.com/dashboard"
    
    # Special case: allow http -> https upgrade on standard ports
    assert session.should_strip_auth(old_url, new_url) is False