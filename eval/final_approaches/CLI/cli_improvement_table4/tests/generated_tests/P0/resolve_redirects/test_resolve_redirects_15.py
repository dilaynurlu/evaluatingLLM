from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import UnrewindableBodyError
import io

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

def test_resolve_redirects_15():
    # Test Rewinding Body
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 307 # Preserve POST
    r0.headers["Location"] = "/new"
    
    # Body with seek support
    body = io.BytesIO(b"data")
    req = Request("POST", "http://example.com/old", data=body).prepare()
    # Mock _body_position
    req._body_position = 0
    
    r0.request = req
    r0.url = "http://example.com/old"
    r0._content = b""
    
    r1 = Response()
    r1.status_code = 200
    r1.url = "http://example.com/new"
    r1._content = b"ok"
    
    session.responses = [r1]
    
    # Move body pointer to simulate read
    body.read()
    assert body.tell() == 4
    
    gen = session.resolve_redirects(r0, r0.request)
    history = list(gen)
    
    # Body should have been rewound
    # The new request uses the same body object?
    # req.copy() does shallow copy of body if it's an object?
    # Actually Request.copy() docs say "Creates a copy of this Request."
    # The implementation of PreparedRequest.copy copies attributes.
    # self.body = self.body (ref copy).
    
    # So if rewind_body called, body.seek(0) happened.
    assert body.tell() == 0
