import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_port_change():
    session = DummySession()
    old = "http://example.com:8080"
    new = "http://example.com:9090"
    assert session.should_strip_auth(old, new) is True
