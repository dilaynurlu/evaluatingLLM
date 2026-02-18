from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import UnrewindableBodyError

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

def test_resolve_redirects_16():
    # Test UnrewindableBodyError
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 307
    r0.headers["Location"] = "/new"
    
    # Body without seek
    # Using generator as unrewindable body
    body = (b"chunk" for _ in range(1))
    
    req = Request("POST", "http://example.com/old", data=body).prepare()
    # If requests doesn't know length, it might try to chunk.
    # We force headers to trigger rewind check
    req.headers["Transfer-Encoding"] = "chunked"
    # _body_position is object() if tell() failed (unrewindable stream usually)
    # or if we just can't record it.
    # requests logic: if _body_position is not None, we try to seek.
    # If tell() failed during prepare, it sets it to object().
    req._body_position = object() 
    
    r0.request = req
    r0.url = "http://example.com/old"
    r0._content = b""
    
    try:
        list(session.resolve_redirects(r0, r0.request))
    except UnrewindableBodyError:
        pass
    else:
        assert False, "Should have raised UnrewindableBodyError"
