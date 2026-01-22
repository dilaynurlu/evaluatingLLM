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

def test_resolve_redirects_14():
    # Test Header Stripping on Method Change (POST 303 -> GET)
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 303
    r0.headers["Location"] = "/new"
    
    # Original request with headers that should be stripped
    headers = {
        "Content-Length": "100",
        "Content-Type": "application/json",
        "Transfer-Encoding": "chunked",
        "X-Custom": "KeepMe"
    }
    r0.request = Request("POST", "http://example.com/old", headers=headers).prepare()
    r0.url = "http://example.com/old"
    r0._content = b""
    
    r1 = Response()
    r1.status_code = 200
    r1.url = "http://example.com/new"
    r1._content = b"ok"
    
    session.responses = [r1]
    
    gen = session.resolve_redirects(r0, r0.request)
    history = list(gen)
    
    new_req = history[0].request
    assert new_req.method == "GET"
    assert "Content-Length" not in new_req.headers
    assert "Content-Type" not in new_req.headers
    assert "Transfer-Encoding" not in new_req.headers
    assert new_req.headers["X-Custom"] == "KeepMe"
    assert new_req.body is None
