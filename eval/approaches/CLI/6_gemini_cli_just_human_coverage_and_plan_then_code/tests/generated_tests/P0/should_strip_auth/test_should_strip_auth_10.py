
import pytest
from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_subdomains():
    mixin = SessionRedirectMixin()
    old_url = "http://api.example.com/foo"
    new_url = "http://www.example.com/bar"
    # Different hostnames
    assert mixin.should_strip_auth(old_url, new_url) is True
