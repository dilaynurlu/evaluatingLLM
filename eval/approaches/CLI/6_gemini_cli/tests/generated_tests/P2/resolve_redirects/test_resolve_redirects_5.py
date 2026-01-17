import pytest
from unittest.mock import Mock
from requests.sessions import SessionRedirectMixin

from requests.cookies import RequestsCookieJar

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.trust_env = True
        self.auth = None
        self.proxies = {}
        self.cookies = RequestsCookieJar()
    def rebuild_method(self, prep, resp): pass
    def rebuild_proxies(self, prep, proxies): return proxies
    def rebuild_auth(self, prep, resp): pass

def test_resolve_redirects_yield_requests():
    session = DummySession()
    req = Mock()
    req.url = "http://example.com"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    resp = Mock()
    resp.is_redirect = True
    resp.url = "http://example.com"
    resp.history = []
    
    session.get_redirect_target = Mock(side_effect=["http://new.com", None])
    
    # In yield_requests=True, send is not called?
    # Logic: if yield_requests: yield req else: resp = self.send(...)
    
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    result = next(gen)
    
    # It yields the prepared request object
    assert result == req
    assert not hasattr(session, 'send') or not session.send.called
