import pytest
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    pass

def test_should_strip_auth_case_insensitive_host():
    session = DummySession()
    old = "http://EXAMPLE.COM"
    new = "http://example.com"
    # urlparse likely handles case, but let's verify.
    # If hostnames strictly equal string-wise?
    # urlparse returns lowercase hostname usually.
    assert session.should_strip_auth(old, new) is False
