import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_same_host():
    """Test auth is kept when host/scheme/port match."""
    mixin = SessionRedirectMixin()
    old = "http://example.com/foo"
    new = "http://example.com/bar"
    assert mixin.should_strip_auth(old, new) is False
