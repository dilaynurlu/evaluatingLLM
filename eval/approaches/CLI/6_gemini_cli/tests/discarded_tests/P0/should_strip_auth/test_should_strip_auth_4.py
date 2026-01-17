
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_https_to_http_downgrade_allowed():
    mixin = SessionRedirectMixin()
    old_url = "https://example.com/foo"
    new_url = "http://example.com/bar"
    # Allowed if ports match defaults for scheme
    assert mixin.should_strip_auth(old_url, new_url) is False
