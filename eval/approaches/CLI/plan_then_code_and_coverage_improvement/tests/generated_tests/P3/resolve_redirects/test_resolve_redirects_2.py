from requests.sessions import Session
from requests.models import Response, PreparedRequest, codes
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_2():
    # POST 303 See Other -> GET
    s = Session()
    s.max_redirects = 3
    
    resp = Response()
    resp.status_code = codes.see_other # 303
    resp.headers["Location"] = "http://example.com/new"
    resp.url = "http://example.com/old"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old"
    resp.request.method = "POST"
    resp.request.headers = {}
    resp.request._cookies = RequestsCookieJar()

    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    def mock_send(req, **kwargs):
        r = Response()
        r.status_code = 200
        r.request = req
        r.raw = MockRaw()
        r._content = b"Done"
        return r
    s.send = mock_send
    
    gen = s.resolve_redirects(resp, resp.request)
    redirects = list(gen)
    
    assert len(redirects) == 1
    # Check that the method changed to GET
    assert redirects[0].request.method == "GET"
