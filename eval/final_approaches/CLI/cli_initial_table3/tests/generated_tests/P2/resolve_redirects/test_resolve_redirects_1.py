import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_301_simple():
    """
    Test a simple 301 redirect.
    """
    mixin = SessionRedirectMixin()
    mixin.max_redirects = 30
    mixin.trust_env = False
    mixin.cookies = RequestsCookieJar()
    
    # Mock methods
    mixin.rebuild_method = MagicMock()
    mixin.rebuild_proxies = MagicMock(return_value={})
    mixin.rebuild_auth = MagicMock()
    
    # Mock initial response
    resp = MagicMock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.history = []
    
    # Mock request
    req = MagicMock()
    req.url = "http://example.com/old"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req.copy.return_value = req
    
    # Mock send
    new_resp = MagicMock()
    new_resp.is_redirect = False
    new_resp.status_code = 200
    mixin.send = MagicMock(return_value=new_resp)
    
    gen = mixin.resolve_redirects(resp, req)
    
    redirects = list(gen)
    
    assert len(redirects) == 1
    assert redirects[0] == new_resp
    mixin.send.assert_called_once()
