from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar

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
    
    def rebuild_proxies(self, r, p): return p

def test_resolve_redirects_12():
    # Test 307 Temporary Redirect (Preserve POST)
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 307
    r0.headers["Location"] = "/new"
    r0.request = Request("POST", "http://example.com/old", data="data").prepare()
    r0.url = "http://example.com/old"
    r0._content = b""
    
    r1 = Response()
    r1.status_code = 200
    r1.url = "http://example.com/new"
    r1._content = b"ok"
    
    session.responses = [r1]
    
    gen = session.resolve_redirects(r0, r0.request)
    history = list(gen)
    
    # Should still be POST
    assert history[0].request.method == "POST"
