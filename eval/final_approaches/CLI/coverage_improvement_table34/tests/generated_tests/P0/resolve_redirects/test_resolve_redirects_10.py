from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar
from requests.utils import cookiejar_from_dict

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

def test_resolve_redirects_10():
    # Test cookie merging from redirect response
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 301
    r0.headers["Location"] = "/new"
    r0.cookies = cookiejar_from_dict({'foo': 'bar'})
    r0.request = Request("GET", "http://example.com/old").prepare()
    r0.url = "http://example.com/old"
    r0._content = b""
    r0.raw = None # Need to avoid issues if extract_cookies tries to use it? 
    # extract_cookies_to_jar uses resp.raw. If we don't mock it, it might fail?
    # In requests 2.x, it might use headers if raw doesn't have msg.
    
    # extract_cookies_to_jar checks for response._original_response.msg
    from http.client import HTTPMessage
    
    class MockOrigResponse:
        def __init__(self):
            self.msg = HTTPMessage()
            self.msg.add_header('Set-Cookie', 'foo=bar; Path=/')
            
    class MockRaw:
        def __init__(self):
            self._original_response = MockOrigResponse()
        
    r0.raw = MockRaw()
    
    r1 = Response()
    r1.status_code = 200
    r1.url = "http://example.com/new"
    r1._content = b"ok"
    
    session.responses = [r1]
    
    gen = session.resolve_redirects(r0, r0.request)
    history = list(gen)
    
    # The new request should have the cookie
    assert "foo=bar" in history[0].request.headers["Cookie"]
