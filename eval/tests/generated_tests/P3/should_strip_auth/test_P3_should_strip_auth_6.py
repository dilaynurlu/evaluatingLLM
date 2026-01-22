import pytest
from requests.sessions import Session

def test_should_strip_auth_strips_on_upgrade_with_non_standard_ports():
    session = Session()
    # Scenario 1: Upgrade with non-standard ports (8080 -> 8443).
    # Requests only allows the specific transition of default ports (80->443) to preserve auth.
    assert session.should_strip_auth("http://example.com:8080/data", "https://example.com:8443/data") is True

    # Scenario 2: Cross-Scheme Standard Port Confusion (Critique 7).
    # http://example.com:443 implies HTTP protocol on port 443. 
    # Redirecting to https://example.com (HTTPS on 443) is a scheme change *and* a logical port usage change.
    assert session.should_strip_auth("http://example.com:443/data", "https://example.com/data") is True