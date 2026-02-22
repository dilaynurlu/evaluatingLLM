import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_yield_requests():
    """
    Test that resolve_redirects yields requests if yield_requests=True.
    """
    mixin = SessionRedirectMixin()
    mixin.max_redirects = 30
    mixin.trust_env = False
    
    mixin.rebuild_method = MagicMock()
    mixin.rebuild_proxies = MagicMock(return_value={})
    mixin.rebuild_auth = MagicMock()
    mixin.cookies = RequestsCookieJar()
    
    # Mock response
    resp = MagicMock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.history = []
    resp.url = "http://example.com/old"
    
    # Mock request
    req = MagicMock()
    req.url = "http://example.com/old"
    req._cookies = RequestsCookieJar()
    req.copy.return_value = req
    
    # We don't need mock send because it yields the request before sending
    
    gen = mixin.resolve_redirects(resp, req, yield_requests=True)
    
    # First yield should be the new request
    new_req = next(gen)
    
    assert new_req.url == "http://example.com/new"