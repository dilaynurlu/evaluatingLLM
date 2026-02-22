import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_relative_url():
    """
    Test resolving a relative redirect URL.
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
    resp.headers = {"location": "/relative"}
    resp.url = "http://example.com/base/"
    resp.history = []
    
    # Mock request
    req = MagicMock()
    req.url = "http://example.com/base/old"
    req._cookies = RequestsCookieJar()
    req.copy.return_value = req
    
    # Mock send
    new_resp = MagicMock()
    new_resp.is_redirect = False
    new_resp.status_code = 200
    new_resp.url = "http://example.com/relative"
    
    mixin.send = MagicMock(return_value=new_resp)
    
    gen = mixin.resolve_redirects(resp, req)
    
    list(gen)
    
    # Check that new request has absolute URL
    args, kwargs = mixin.send.call_args
    new_req = args[0]
    # urljoin("http://example.com/base/", "/relative") -> "http://example.com/relative"
    assert new_req.url == "http://example.com/relative"