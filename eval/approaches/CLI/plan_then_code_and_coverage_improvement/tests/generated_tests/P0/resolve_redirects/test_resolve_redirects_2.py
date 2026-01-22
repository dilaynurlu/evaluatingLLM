from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects
from requests.cookies import RequestsCookieJar
from collections import OrderedDict

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 2
        self.cookies = RequestsCookieJar()
        self.trust_env = False
        self.auth = None
        self.proxies = {}
        self.responses = []

    def send(self, request, **kwargs):
        # Always redirect
        resp = Response()
        resp.status_code = 301
        resp.headers["Location"] = "http://example.com/next"
        resp.url = request.url
        resp.request = request
        resp._content = b""
        return resp
        
    def rebuild_proxies(self, prepared_request, proxies):
        return proxies

def test_resolve_redirects_2():
    # Test TooManyRedirects
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 301
    r0.headers["Location"] = "http://example.com/1"
    r0.request = Request("GET", "http://example.com/0").prepare()
    r0.url = "http://example.com/0"
    r0._content = b""
    
    try:
        list(session.resolve_redirects(r0, r0.request))
    except TooManyRedirects as e:
        assert "Exceeded 2 redirects" in str(e)
    else:
        assert False, "Should have raised TooManyRedirects"
