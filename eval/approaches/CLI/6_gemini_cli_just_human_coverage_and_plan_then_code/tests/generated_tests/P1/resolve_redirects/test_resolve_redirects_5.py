import pytest
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.cookies = RequestsCookieJar()
        self.trust_env = False
        
    def rebuild_auth(self, prepared_request, response): pass
    def rebuild_proxies(self, prepared_request, proxies): return proxies
    def send(self, request, **kwargs):
        resp = Mock()
        resp.url = request.url
        resp.status_code = 200
        resp.is_redirect = False
        resp.headers = {}
        return resp

def test_resolve_redirects_post_303():
    session = MockSession()
    
    resp = Mock()
    resp.url = "http://example.com/old"
    resp.status_code = 303
    resp.is_redirect = True
    resp.headers = {"location": "/new"}
    resp.history = []
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/old"
    req.method = "POST"
    req.headers = {}
    req.copy = Mock(return_value=req)
    req._cookies = RequestsCookieJar()
    
    gen = session.resolve_redirects(resp, req)
    history = list(gen)
    
    # 303 -> GET
    assert req.method == "GET" 
    assert history[0].url == "http://example.com/new"