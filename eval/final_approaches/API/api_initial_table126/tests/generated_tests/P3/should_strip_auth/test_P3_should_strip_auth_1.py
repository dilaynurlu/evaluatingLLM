import pytest
from requests.sessions import Session

def test_should_strip_auth_strips_on_hostname_change():
    session = Session()
    # Scenario 1: Completely different domains.
    assert session.should_strip_auth("http://example.com/r", "http://other-domain.com/r") is True

    # Scenario 2: Subdomain changes (Critique 1).
    # Different subdomains are different origins; auth should be stripped.
    assert session.should_strip_auth("http://user1.example.com/r", "http://user2.example.com/r") is True
    assert session.should_strip_auth("http://www.example.com/r", "http://api.example.com/r") is True

    # Scenario 3: Localhost vs Loopback IP (Critique 3).
    # These are technically different hosts in the eyes of the browser/client, 
    # and treating them as the same can be a security risk (DNS rebinding, etc).
    assert session.should_strip_auth("http://localhost/r", "http://127.0.0.1/r") is True
    
    # Scenario 4: Visual spoofing / IDNA (Critique 6).
    # 'exämple.com' is not 'example.com'.
    assert session.should_strip_auth("http://example.com/r", "http://exämple.com/r") is True