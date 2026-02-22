import pytest
from requests.sessions import Session
from requests.models import Response, Request
from requests.exceptions import TooManyRedirects

class MockSession(Session):
    def send(self, request, **kwargs):
        # Always return redirect
        r = Response()
        r.status_code = 302
        r.headers["Location"] = "/loop"
        r.url = request.url
        r.request = request
        return r

def test_resolve_redirects_2():
    s = MockSession()
    s.max_redirects = 2
    
    r1 = Response()
    r1.status_code = 302
    r1.headers["Location"] = "/loop"
    r1.url = "http://example.com/"
    
    req = Request("GET", "http://example.com/")
    prep = s.prepare_request(req)
    r1.request = prep
    
    with pytest.raises(TooManyRedirects):
        list(s.resolve_redirects(r1, prep))
