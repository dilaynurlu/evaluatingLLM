import pytest
from requests.sessions import SessionRedirectMixin
from requests.cookies import RequestsCookieJar
from requests.exceptions import TooManyRedirects
from unittest.mock import Mock

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 1 # Set low limit
        self.cookies = RequestsCookieJar()
        self.trust_env = False
        
    def rebuild_auth(self, prepared_request, response): pass
    def rebuild_proxies(self, prepared_request, proxies): return proxies
    def send(self, request, **kwargs):
        # Always return redirect
        resp = Mock()
        resp.url = request.url
        resp.status_code = 301
        resp.is_redirect = True
        resp.headers = {"location": "http://example.com/next"}
        return resp

def test_resolve_redirects_max_exceeded():
    session = MockSession()
    
    resp = Mock()
    resp.url = "http://example.com/start"
    resp.status_code = 301
    resp.is_redirect = True
    resp.headers = {"location": "http://example.com/next"}
    resp.history = []
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/start"
    req.headers = {}
    req.copy = Mock(return_value=req)
    req._cookies = RequestsCookieJar()
    
    with pytest.raises(TooManyRedirects):
        list(session.resolve_redirects(resp, req))