import pytest
from requests.sessions import Session

def test_should_strip_auth_upgrade_failure_non_standard_port():
    """
    Test that Authorization header is stripped when upgrading HTTP to HTTPS
    if the ports are NOT the standard ones (e.g. http:8080 -> https).
    This ensures the special case logic strictly enforces standard ports.
    """
    session = Session()
    # Old port is 8080, not 80 or None.
    old_url = "http://example.com:8080/foo"
    new_url = "https://example.com/foo"
    
    # Upgrade but from non-standard port -> should strip auth (special case doesn't apply)
    assert session.should_strip_auth(old_url, new_url) is True