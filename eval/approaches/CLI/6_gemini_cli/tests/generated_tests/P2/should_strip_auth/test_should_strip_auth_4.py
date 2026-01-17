import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_downgrade():
    session = DummySession()
    old = "https://example.com"
    new = "http://example.com"
    # Should strip (changed scheme and not upgraded)
    assert session.should_strip_auth(old, new) is True
