import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_different_host():
    session = DummySession()
    old = "http://example.com"
    new = "http://other.com"
    assert session.should_strip_auth(old, new) is True
