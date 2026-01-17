import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_default_port():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com/foo" # Port None (80 implied)
    new_url = "http://example.com:80/foo"
    assert mixin.should_strip_auth(old_url, new_url) is False
