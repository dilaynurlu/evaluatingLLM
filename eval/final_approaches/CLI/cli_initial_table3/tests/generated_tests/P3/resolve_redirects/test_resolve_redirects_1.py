import pytest
from requests.sessions import Session
from requests.models import Response, Request
from requests.exceptions import TooManyRedirects

class MockSession(Session):
    def __init__(self, responses):
        super().__init__()
        self.responses = responses
        self.call_count = 0

    def send(self, request, **kwargs):
        if self.call_count < len(self.responses):
            resp = self.responses[self.call_count]
            resp.request = request
            self.call_count += 1
            return resp
        return Response() # Default

def test_resolve_redirects_1():
    # Setup chain: 301 -> 200
    r1 = Response()
    r1.status_code = 301
    r1.headers["Location"] = "/target"
    r1.url = "http://example.com/source"
    
    r2 = Response()
    r2.status_code = 200
    r2.url = "http://example.com/target"
    
    s = MockSession([r2])
    
    req = Request("GET", "http://example.com/source")
    prep = s.prepare_request(req)
    r1.request = prep
    
    gen = s.resolve_redirects(r1, prep)
    history = list(gen)
    
    assert len(history) == 1
    assert history[0] == r2
    assert history[0].status_code == 200
