
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_default_to_explicit_port_https():
    mixin = SessionRedirectMixin()
    old_url = "https://example.com/foo"
    new_url = "https://example.com:443/bar"
    assert mixin.should_strip_auth(old_url, new_url) is False
