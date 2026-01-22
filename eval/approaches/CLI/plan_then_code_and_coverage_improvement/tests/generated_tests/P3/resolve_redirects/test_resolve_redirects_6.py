from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_6():
    # yield_requests=True
    s = Session()
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "http://example.com/new"
    resp.url = "http://example.com/old"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old"
    resp.request.method = "GET"
    resp.request.headers = {}
    resp.request._cookies = RequestsCookieJar()
    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    # If yield_requests is True, the generator yields the request but doesn't update 'url' or 'resp'
    # causing an infinite loop if we iterate it all. We just want to check the first yielded request.
    gen = s.resolve_redirects(resp, resp.request, yield_requests=True)
    req = next(gen)
    
    assert isinstance(req, PreparedRequest)
    assert req.url == "http://example.com/new"
