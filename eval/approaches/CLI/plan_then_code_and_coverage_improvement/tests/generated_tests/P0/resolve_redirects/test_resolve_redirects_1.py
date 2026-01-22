from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar
from collections import OrderedDict

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.cookies = RequestsCookieJar()
        self.trust_env = False
        self.auth = None
        self.proxies = {}
        self.responses = []
    
    def send(self, request, **kwargs):
        if self.responses:
            resp = self.responses.pop(0)
            resp.request = request
            return resp
        return None

    def rebuild_proxies(self, prepared_request, proxies):
        return proxies

def test_resolve_redirects_1():
    # Test single 301 redirect
    session = MockSession()
    
    # Initial response causing redirect
    r0 = Response()
    r0.status_code = 301
    r0.headers["Location"] = "http://example.com/new"
    r0.request = Request("GET", "http://example.com/old").prepare()
    r0.url = "http://example.com/old"
    
    # Next response (success)
    r1 = Response()
    r1.status_code = 200
    r1.url = "http://example.com/new"
    r1._content = b"ok"
    
    session.responses = [r1]
    
    gen = session.resolve_redirects(r0, r0.request)
    history = list(gen)
    
    assert len(history) == 1
    assert history[0].status_code == 200
    assert history[0].url == "http://example.com/new"
