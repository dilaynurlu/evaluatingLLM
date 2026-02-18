import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_diff_port():
    """Test auth is stripped when port changes."""
    mixin = SessionRedirectMixin()
    old = "http://example.com:8080/foo"
    new = "http://example.com:9090/foo"
    assert mixin.should_strip_auth(old, new) is True
