import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_diff_host():
    """Test auth is stripped when hostnames differ."""
    mixin = SessionRedirectMixin()
    old = "http://example.com/foo"
    new = "http://other.com/foo"
    assert mixin.should_strip_auth(old, new) is True
