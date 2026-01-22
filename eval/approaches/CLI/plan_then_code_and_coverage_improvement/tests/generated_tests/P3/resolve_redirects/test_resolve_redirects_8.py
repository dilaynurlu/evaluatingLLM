from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_8():
    # Test purging headers on redirect (Content-Length etc.)
    # When 301/302/303 and method becomes GET, body headers should be removed.
    
    s = Session()
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/new"
    resp.url = "http://example.com/old"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old"
    resp.request.method = "POST"
    resp.request.headers = {"Content-Length": "100", "Content-Type": "text/plain", "Transfer-Encoding": "chunked", "User-Agent": "test"}
    from requests.cookies import RequestsCookieJar
    resp.request._cookies = RequestsCookieJar()
    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    gen = s.resolve_redirects(resp, resp.request, yield_requests=True)
    req = next(gen)
    
    assert req.method == "GET"
    assert "Content-Length" not in req.headers
    assert "Content-Type" not in req.headers
    assert "Transfer-Encoding" not in req.headers
    assert "User-Agent" in req.headers
