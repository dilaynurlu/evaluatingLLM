
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_different_port_custom():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com:8080/foo"
    new_url = "http://example.com:9090/bar"
    assert mixin.should_strip_auth(old_url, new_url) is True
