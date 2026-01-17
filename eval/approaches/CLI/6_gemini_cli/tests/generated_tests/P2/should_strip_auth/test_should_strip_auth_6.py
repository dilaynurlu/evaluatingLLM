import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_default_port():
    session = DummySession()
    old = "http://example.com"     # port None (implies 80)
    new = "http://example.com:80"  # port 80
    assert session.should_strip_auth(old, new) is False
