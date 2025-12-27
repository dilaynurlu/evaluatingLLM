import pytest
from requests.sessions import Session

def test_should_strip_auth_implicit_explicit_default_port():
    session = Session()
    # http scheme implies port 80
    old_url = "http://example.com/page"
    # Explicitly specifying port 80 for http
    new_url = "http://example.com:80/page"
    
    # Scenario: Redirecting between implicit and explicit default ports.
    # Expected behavior: Authorization headers should NOT be stripped as it is effectively the same port (return False).
    assert session.should_strip_auth(old_url, new_url) is False