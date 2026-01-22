from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_1():
    # Simple redirect
    # We need to mock Session.send to return a final response
    # resolve_redirects yields responses.
    
    s = Session()
    s.max_redirects = 3
    
    # Original response (301)
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/new"
    resp.url = "http://example.com/old"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/old"
    resp.request.method = "GET"
    resp.request.headers = {}
    resp.request._cookies = RequestsCookieJar()

    
    # Mock connection for release
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    # Mock send
    def mock_send(req, **kwargs):
        r = Response()
        r.status_code = 200
        r.url = req.url
        r.request = req
        r.raw = MockRaw()
        r._content = b"Done"
        return r
    
    s.send = mock_send
    
    # Call resolve_redirects
    gen = s.resolve_redirects(resp, resp.request)
    redirects = list(gen)
    
    assert len(redirects) == 1
    assert redirects[0].status_code == 200
    assert redirects[0].url == "http://example.com/new"