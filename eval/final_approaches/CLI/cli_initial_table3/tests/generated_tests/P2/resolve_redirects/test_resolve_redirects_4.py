import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_get_redirect_target():
    """
    Test interaction with get_redirect_target.
    """
    mixin = SessionRedirectMixin()
    mixin.max_redirects = 30
    mixin.trust_env = False
    mixin.cookies = RequestsCookieJar()
    
    # Mock methods
    mixin.rebuild_method = MagicMock()
    mixin.rebuild_proxies = MagicMock(return_value={})
    mixin.rebuild_auth = MagicMock()
    
    # Mock response
    resp = MagicMock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.history = []
    resp.url = "http://example.com/old"
    
    # Mock request
    req = MagicMock()
    req.url = "http://example.com/old"
    req._cookies = RequestsCookieJar()
    req.copy.return_value = req
    
    # Mock send
    new_resp = MagicMock()
    new_resp.is_redirect = False
    new_resp.url = "http://example.com/new"
    
    mixin.send = MagicMock(return_value=new_resp)
    
    # Mock get_redirect_target to return a specific URL
    mixin.get_redirect_target = MagicMock(side_effect=["http://example.com/new", None])
    
    gen = mixin.resolve_redirects(resp, req)
    
    redirects = list(gen)
    
    assert len(redirects) == 1
    assert redirects[0] == new_resp
    
    mixin.get_redirect_target.assert_any_call(resp)
    mixin.get_redirect_target.assert_any_call(new_resp)