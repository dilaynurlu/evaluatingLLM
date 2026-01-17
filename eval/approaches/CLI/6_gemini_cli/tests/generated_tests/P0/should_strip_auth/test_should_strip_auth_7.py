
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_default_to_explicit_port_http():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com/foo"
    new_url = "http://example.com:80/bar"
    # Should recognize 80 is default for http
    assert mixin.should_strip_auth(old_url, new_url) is False
