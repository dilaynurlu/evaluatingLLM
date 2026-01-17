import pytest
from unittest.mock import Mock
from requests.sessions import SessionRedirectMixin
from requests.exceptions import TooManyRedirects

from requests.cookies import RequestsCookieJar

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 1 # Set low limit
        self.trust_env = True
        self.auth = None
        self.proxies = {}
        self.cookies = RequestsCookieJar()
    
    def rebuild_method(self, prep, resp): pass
    def rebuild_proxies(self, prep, proxies): return proxies
    def rebuild_auth(self, prep, resp): pass

def test_resolve_redirects_too_many():
    session = DummySession()
    
    req = Mock()
    req.url = "http://example.com"
    req.copy.return_value = req
    req.headers = {}
    req._cookies = RequestsCookieJar()

    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/2"}
    resp.url = "http://example.com"
    resp.history = [] # Empty history initially

    # If we loop, history grows.
    # Logic in resolve_redirects:
    # hist.append(resp)
    # resp.history = hist[1:]
    # if len(resp.history) >= self.max_redirects: raise
    
    # We need to simulate the history growth.
    # But since we control the loop via get_redirect_target, we can just make it infinite
    session.get_redirect_target = Mock(return_value="http://example.com/next")
    
    # Mock send to return a response that also redirects
    def side_effect_send(*args, **kwargs):
        r = Mock()
        r.is_redirect = True
        r.status_code = 301
        r.url = args[0].url
        r.history = [] # Will be set by loop
        return r
    session.send = Mock(side_effect=side_effect_send)

    with pytest.raises(TooManyRedirects):
        list(session.resolve_redirects(resp, req))
