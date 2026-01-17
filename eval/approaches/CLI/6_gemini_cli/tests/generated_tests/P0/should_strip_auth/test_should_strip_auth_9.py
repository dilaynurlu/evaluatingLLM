
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_explicit_to_default_port():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com:80/foo"
    new_url = "http://example.com/bar"
    assert mixin.should_strip_auth(old_url, new_url) is False
