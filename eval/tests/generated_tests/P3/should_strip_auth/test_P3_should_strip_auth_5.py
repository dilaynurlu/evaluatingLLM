import pytest
from requests.sessions import Session

def test_should_strip_auth_allows_implicit_to_explicit_default_port():
    session = Session()
    # Scenario 1: HTTP implicit (None) to explicit (80).
    assert session.should_strip_auth("http://example.com/r", "http://example.com:80/r") is False
    
    # Scenario 2: HTTPS implicit (None) to explicit (443) (Critique 5).
    # This ensures SSL/TLS default ports are handled correctly.
    assert session.should_strip_auth("https://example.com/r", "https://example.com:443/r") is False

    # Scenario 3: Explicit default to implicit.
    assert session.should_strip_auth("https://example.com:443/r", "https://example.com/r") is False