from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_4():
    # Relative redirect
    s = Session()
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "/relative/path"
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
    
    assert len(redirects) == 1
    assert redirects[0].url == "http://example.com/relative/path"
