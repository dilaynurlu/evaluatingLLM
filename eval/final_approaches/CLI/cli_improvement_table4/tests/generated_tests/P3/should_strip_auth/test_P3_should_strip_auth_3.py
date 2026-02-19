import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_http_to_https():
    mixin = SessionRedirectMixin()
    old = "http://example.com/old"
    new = "https://example.com/new"
    assert mixin.should_strip_auth(old, new) is False
