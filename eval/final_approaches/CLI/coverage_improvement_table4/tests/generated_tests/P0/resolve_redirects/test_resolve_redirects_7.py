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

def test_resolve_redirects_7():
    # Test with stream=True
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 301
    r0.headers["Location"] = "/new"
    r0.request = Request("GET", "http://example.com/old").prepare()
    r0.url = "http://example.com/old"
    r0._content = b""
    
    r1 = Response()
    r1.status_code = 200
    r1.url = "http://example.com/new"
    # Content should not be consumed immediately if stream=True involved?
    # Actually resolve_redirects calls r.content on the *redirect response* to consume it,
    # but the *final* response is yielded.
    r1._content = b"ok"
    
    session.responses = [r1]
    
    gen = session.resolve_redirects(r0, r0.request, stream=True)
    history = list(gen)
    
    assert history[0].status_code == 200
    # Implementation detail: resolve_redirects accesses .content if not stream
    # If stream=True, it might not read content of the *yielded* response inside the generator?
    # The code says: if not stream: r.content
    # So we check if content was read or not? 
    # Hard to check side effect on r1.content without mocking property.
    # But we can verify it runs without error.
