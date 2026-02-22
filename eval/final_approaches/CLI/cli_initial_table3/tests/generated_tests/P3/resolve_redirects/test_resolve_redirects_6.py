import pytest
from requests.sessions import Session
from requests.models import Response, Request, PreparedRequest

class MockSession(Session):
    def send(self, request, **kwargs):
        r = Response()
        r.status_code = 200
        r.url = request.url
        r.request = request
        return r

def test_resolve_redirects_yield_requests():
    s = MockSession()
    
    r1 = Response()
    r1.status_code = 301
    r1.headers["Location"] = "/target"
    r1.url = "http://example.com/source"
    
    req = Request("GET", "http://example.com/source")
    prep = s.prepare_request(req)
    r1.request = prep
    
    gen = s.resolve_redirects(r1, prep, yield_requests=True)
    
    item = next(gen)
    assert isinstance(item, PreparedRequest)
    assert item.url == "http://example.com/target"
