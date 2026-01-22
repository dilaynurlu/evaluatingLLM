import pytest
from requests.sessions import Session

def test_should_strip_auth_on_non_standard_http_to_https_upgrade():
    """
    Test that Authorization header is stripped when upgrading HTTP to HTTPS 
    if non-standard ports are involved, as the special exemption only applies 
    to standard ports (80/443).
    """
    session = Session()
    old_url = "http://example.com:8080/foo"
    new_url = "https://example.com:8443/foo"
    
    # Logic:
    # Hostnames match.
    # Special case check: old port 8080 not in (80, None). Fails.
    # Default port check: schemes differ. Fails.
    # Returns changed_scheme (True) or changed_port (True) -> True.
    assert session.should_strip_auth(old_url, new_url) is True