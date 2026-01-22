from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects
from requests.cookies import RequestsCookieJar
import pytest

def test_resolve_redirects_3():
    # Too many redirects
    s = Session()
    s.max_redirects = 1 # Only 1 allowed
    
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/1"
    resp.url = "http://example.com/0"
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/0"
    resp.request.method = "GET"
    resp.request.headers = {}
    resp.request._cookies = RequestsCookieJar()

    
    class MockRaw:
        def read(self, **kwargs): return b""
    resp.raw = MockRaw()
    resp._content = b""
    
    # Send returns another redirect
    def mock_send(req, **kwargs):
        r = Response()
        r.status_code = 301
        r.headers["Location"] = "http://example.com/2" # Next one
        r.url = req.url
        r.request = req
        r.raw = MockRaw()
        r._content = b""
        return r
    s.send = mock_send
    
    # The first redirect works (0->1). The second (1->2) should fail if max_redirects is exceeded?
    # Logic: if len(resp.history) >= self.max_redirects: raise
    # History grows.
    
    with pytest.raises(TooManyRedirects):
        # We need to iterate to trigger the loop
        for _ in s.resolve_redirects(resp, resp.request):
            pass