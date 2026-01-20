import pytest
from unittest.mock import Mock
from requests.sessions import SessionRedirectMixin
from requests.status_codes import codes

from requests.cookies import RequestsCookieJar

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.trust_env = True
        self.auth = None
        self.proxies = {}
        self.cookies = RequestsCookieJar()
    def rebuild_proxies(self, prep, proxies): return proxies
    def rebuild_auth(self, prep, resp): pass
    # We use real rebuild_method from Mixin

def test_resolve_redirects_303_post_to_get():
    session = DummySession()
    req = Mock()
    req.method = "POST"
    req.url = "http://example.com"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = codes.see_other # 303
    resp.url = "http://example.com"
    resp.history = []
    
    session.get_redirect_target = Mock(side_effect=["http://new.com", None])
    resp2 = Mock()
    resp2.is_redirect = False
    session.send = Mock(return_value=resp2)
    
    list(session.resolve_redirects(resp, req))
    
    args, _ = session.send.call_args
    assert args[0].method == "GET"
