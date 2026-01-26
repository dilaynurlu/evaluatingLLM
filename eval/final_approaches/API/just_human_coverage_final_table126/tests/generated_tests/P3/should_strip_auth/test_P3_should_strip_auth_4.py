import pytest
from requests.sessions import Session

def test_should_strip_auth_strips_on_port_change_same_scheme():
    session = Session()
    # Scenario 1: Explicit port change (e.g., 8080 -> 9090).
    assert session.should_strip_auth("http://example.com:8080/api", "http://example.com:9090/api") is True

    # Scenario 2: Implicit default to explicit non-standard.
    # e.g., http://example.com (port 80) -> http://example.com:8080.
    assert session.should_strip_auth("http://example.com/api", "http://example.com:8080/api") is True