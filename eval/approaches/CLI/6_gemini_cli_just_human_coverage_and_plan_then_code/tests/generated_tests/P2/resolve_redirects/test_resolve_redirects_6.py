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

def test_resolve_redirects_302_found():
    session = DummySession()
    req = Mock()
    req.method = "POST"
    req.url = "http://example.com"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = codes.found # 302
    resp.url = "http://example.com"
    resp.history = []
    
    session.get_redirect_target = Mock(side_effect=["http://new.com", None])
    session.send = Mock(return_value=Mock(is_redirect=False))
    
    list(session.resolve_redirects(resp, req))
    
    # 302 converts POST to GET (browser behavior)
    args, _ = session.send.call_args
    assert args[0].method == "GET"
