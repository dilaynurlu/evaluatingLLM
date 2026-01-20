import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_http_https_custom_ports():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com:8080/foo"
    new_url = "https://example.com:8443/foo"
    assert mixin.should_strip_auth(old_url, new_url) is True
