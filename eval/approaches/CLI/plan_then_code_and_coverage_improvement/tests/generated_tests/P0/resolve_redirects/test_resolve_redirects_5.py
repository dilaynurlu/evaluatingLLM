from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response, PreparedRequest
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
        # Should not be called if yield_requests=True
        return None
        
    def rebuild_proxies(self, prepared_request, proxies):
        return proxies

def test_resolve_redirects_5():
    # Test yield_requests=True
    session = MockSession()
    
    r0 = Response()
    r0.status_code = 302
    r0.headers["Location"] = "http://example.com/next"
    r0.request = Request("GET", "http://example.com/start").prepare()
    r0.url = "http://example.com/start"
    r0._content = b""
    
    gen = session.resolve_redirects(r0, r0.request, yield_requests=True)
    item = next(gen)
    
    assert isinstance(item, PreparedRequest)
    assert item.url == "http://example.com/next"
