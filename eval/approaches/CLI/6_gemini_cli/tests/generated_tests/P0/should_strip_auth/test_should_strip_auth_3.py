
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_http_to_https_upgrade():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com/foo"
    new_url = "https://example.com/bar"
    # Port changes from 80 (implied) to 443 (implied) but this is whitelisted
    assert mixin.should_strip_auth(old_url, new_url) is False
