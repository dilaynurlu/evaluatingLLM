import pytest
from requests.sessions import Session
from requests.models import Response, Request

class MockSession(Session):
    def send(self, request, **kwargs):
        r = Response()
        r.status_code = 200
        r.url = request.url
        r.request = request
        return r

def test_resolve_redirects_303():
    # 303 See Other: POST -> GET always
    s = MockSession()
    
    r1 = Response()
    r1.status_code = 303
    r1.headers["Location"] = "/target"
    r1.url = "http://example.com/source"
    
    req = Request("POST", "http://example.com/source", data="foo")
    prep = s.prepare_request(req)
    r1.request = prep
    
    gen = s.resolve_redirects(r1, prep)
    final_resp = next(gen)
    
    assert final_resp.request.method == "GET"
    assert final_resp.request.body is None
