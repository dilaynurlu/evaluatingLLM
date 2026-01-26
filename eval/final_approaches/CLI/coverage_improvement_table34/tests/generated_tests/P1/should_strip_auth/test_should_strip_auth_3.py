import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_http_https_upgrade():
    """Test auth is kept when upgrading http to https on standard ports."""
    mixin = SessionRedirectMixin()
    old = "http://example.com/foo"
    new = "https://example.com/foo"
    assert mixin.should_strip_auth(old, new) is False
