from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_9():
    # Test 307 Temporary Redirect (method preservation)
    s = Session()
    resp = Response()
    resp.status_code = 307
    resp.headers["Location"] = "http://example.com/new"
    resp.url = "http://example.com/old"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old"
    resp.request.method = "POST"
    resp.request.headers = {"Content-Length": "100"}
    from requests.cookies import RequestsCookieJar
    resp.request._cookies = RequestsCookieJar()
    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    gen = s.resolve_redirects(resp, resp.request, yield_requests=True)
    req = next(gen)
    
    assert req.method == "POST"
    # Headers should be preserved (except Cookie which is handled separately)
    assert "Content-Length" in req.headers
