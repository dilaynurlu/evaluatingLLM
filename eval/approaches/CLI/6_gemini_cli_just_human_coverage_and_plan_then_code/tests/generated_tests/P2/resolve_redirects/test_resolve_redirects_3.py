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

def test_resolve_redirects_relative():
    session = DummySession()
    req = Mock()
    req.url = "http://example.com/foo"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    resp = Mock()
    resp.is_redirect = True
    resp.url = "http://example.com/foo"
    resp.history = []
    
    # Relative path
    session.get_redirect_target = Mock(side_effect=["/bar", None])
    
    resp2 = Mock()
    resp2.is_redirect = False
    session.send = Mock(return_value=resp2)
    
    list(session.resolve_redirects(resp, req))
    
    # Check that the new request url is combined correctly
    # args[0] is the prepared request passed to send
    args, _ = session.send.call_args
    assert args[0].url == "http://example.com/bar"
