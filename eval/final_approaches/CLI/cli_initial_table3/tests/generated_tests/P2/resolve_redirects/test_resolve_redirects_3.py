import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_fragment_preserved():
    """
    Test that fragment is preserved across redirects.
    """
    mixin = SessionRedirectMixin()
    mixin.max_redirects = 30
    mixin.trust_env = False
    
    mixin.rebuild_method = MagicMock()
    mixin.rebuild_proxies = MagicMock(return_value={})
    mixin.rebuild_auth = MagicMock()
    mixin.cookies = RequestsCookieJar()
    
    # Initial response
    resp = MagicMock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.history = []
    resp.url = "http://example.com/old"
    
    # Initial request with fragment
    req = MagicMock()
    req.url = "http://example.com/old#frag"
    req._cookies = RequestsCookieJar()
    req.copy.return_value = req
    
    # Next response
    new_resp = MagicMock()
    new_resp.is_redirect = False
    new_resp.status_code = 200
    new_resp.url = "http://example.com/new#frag"
    
    # Mock send
    mixin.send = MagicMock(return_value=new_resp)
    
    gen = mixin.resolve_redirects(resp, req)
    
    list(gen)
    
    # Check that new request has fragment
    args, kwargs = mixin.send.call_args
    new_req = args[0]
    assert new_req.url == "http://example.com/new#frag"