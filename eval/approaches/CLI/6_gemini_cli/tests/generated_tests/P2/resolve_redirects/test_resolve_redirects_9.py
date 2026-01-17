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

def test_resolve_redirects_fragment_override():
    session = DummySession()
    req = Mock()
    req.url = "http://example.com/start#old"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    resp = Mock()
    resp.is_redirect = True
    resp.url = "http://example.com/start"
    resp.history = []
    
    # Redirect to URL WITH new fragment
    session.get_redirect_target = Mock(side_effect=["http://new.com/page#new", None])
    session.send = Mock(return_value=Mock(is_redirect=False))
    
    list(session.resolve_redirects(resp, req))
    
    args, _ = session.send.call_args
    assert args[0].url == "http://new.com/page#new"
