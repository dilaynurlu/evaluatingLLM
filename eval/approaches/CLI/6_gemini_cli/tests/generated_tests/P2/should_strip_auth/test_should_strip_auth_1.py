import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_same_host():
    session = DummySession()
    old = "http://example.com/foo"
    new = "http://example.com/bar"
    assert session.should_strip_auth(old, new) is False
