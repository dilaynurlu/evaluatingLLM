from requests.sessions import SessionRedirectMixin, Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_7():
    # Redirect with "Location: //host/path" (scheme relative)
    s = Session()
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "//example.com/new"
    resp.url = "http://example.com/old"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old"
    resp.request.method = "GET"
    resp.request.headers = {}
    from requests.cookies import RequestsCookieJar
    resp.request._cookies = RequestsCookieJar()
    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    gen = s.resolve_redirects(resp, resp.request, yield_requests=True)
    req = next(gen)
    
    # Should pick up "http" from original request
    assert req.url == "http://example.com/new"
