import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_https_http():
    mixin = SessionRedirectMixin()
    old_url = "https://example.com/foo"
    new_url = "http://example.com/foo"
    assert mixin.should_strip_auth(old_url, new_url) is True
