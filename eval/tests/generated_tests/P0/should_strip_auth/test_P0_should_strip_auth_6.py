import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_non_standard_ports():
    session = Session()
    # Non-standard http port
    old_url = "http://example.com:8080/start"
    # Non-standard https port
    new_url = "https://example.com:8443/end"
    
    # Scenario: Upgrading from HTTP to HTTPS but using non-standard ports.
    # This falls outside the special backwards compatibility check for standard ports.
    # Expected behavior: Authorization headers should be stripped (return True).
    assert session.should_strip_auth(old_url, new_url) is True