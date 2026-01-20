import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_diff_host():
    mixin = SessionRedirectMixin()
    old_url = "http://example.com/foo"
    new_url = "http://other.com/foo"
    assert mixin.should_strip_auth(old_url, new_url) is True
