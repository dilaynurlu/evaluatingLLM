from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_5():
    # Fragment handling
    s = Session()
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "http://example.com/new"
    # Old URL has fragment
    resp.url = "http://example.com/old#frag"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old#frag"
    resp.request.method = "GET"
    resp.request.headers = {}
    resp.request._cookies = RequestsCookieJar()
    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    def mock_send(req, **kwargs):
        r = Response()
        r.status_code = 200
        r.url = req.url
        r.request = req
        r.raw = MockRaw()
        r._content = b""
        return r
    s.send = mock_send
    
    gen = s.resolve_redirects(resp, resp.request)
    redirects = list(gen)
    
    # Fragment should be preserved
    assert redirects[0].url == "http://example.com/new#frag"
