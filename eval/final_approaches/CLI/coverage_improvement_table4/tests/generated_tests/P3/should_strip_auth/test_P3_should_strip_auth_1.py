import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_same_host():
    mixin = SessionRedirectMixin()
    old = "http://example.com/old"
    new = "http://example.com/new"
    assert mixin.should_strip_auth(old, new) is False
