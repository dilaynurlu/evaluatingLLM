import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_http_to_https():
    session = DummySession()
    old = "http://example.com"
    new = "https://example.com"
    # Special case allow
    assert session.should_strip_auth(old, new) is False
