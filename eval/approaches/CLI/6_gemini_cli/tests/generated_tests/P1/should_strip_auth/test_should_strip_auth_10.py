import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_https_https_port_change():
    mixin = SessionRedirectMixin()
    old_url = "https://example.com/foo"
    new_url = "https://example.com:8443/foo"
    assert mixin.should_strip_auth(old_url, new_url) is True
