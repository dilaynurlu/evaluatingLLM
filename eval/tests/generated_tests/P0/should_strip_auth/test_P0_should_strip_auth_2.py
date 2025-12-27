import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_standard_upgrade():
    session = Session()
    # Implicit port 80 for http
    old_url = "http://example.com/login"
    # Implicit port 443 for https
    new_url = "https://example.com/dashboard"
    
    # Scenario: Upgrading from HTTP to HTTPS on standard ports (legacy/compatibility support).
    # Expected behavior: Authorization headers should NOT be stripped (return False).
    assert session.should_strip_auth(old_url, new_url) is False