import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import SessionRedirectMixin

from requests.cookies import RequestsCookieJar

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.trust_env = True
        self.auth = None
        self.proxies = {}
        self.cookies = RequestsCookieJar()
    
    def rebuild_method(self, prep, resp):
        pass
    def rebuild_proxies(self, prep, proxies):
        return proxies
    def rebuild_auth(self, prep, resp):
        pass

def test_resolve_redirects_simple_301():
    session = DummySession()
    
    # Original Request
    req = Mock()
    req.url = "http://example.com"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    # Response 1 (301)
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.url = "http://example.com"
    resp.history = []
    
    # Next Response (200)
    resp2 = Mock()
    resp2.is_redirect = False
    resp2.status_code = 200
    resp2.url = "http://example.com/new"
    resp2.history = []
    
    # Mock send to return resp2 when called
    session.send = Mock(return_value=resp2)
    
    # Mock get_redirect_target
    # First call returns new url, second call returns None (stop)
    session.get_redirect_target = Mock(side_effect=["http://example.com/new", None])
    
    gen = session.resolve_redirects(resp, req)
    history = list(gen)
    
    assert len(history) == 1
    assert history[0] == resp2
    assert session.send.called
