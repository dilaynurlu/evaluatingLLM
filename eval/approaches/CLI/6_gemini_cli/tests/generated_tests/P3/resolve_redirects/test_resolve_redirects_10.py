from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_yield_requests():
    s = Session()
    s.send = Mock() # Should NOT be called
    
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "/new"
    resp.url = "http://example.com/old"
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    # Gen should yield the prepared request for the redirect, not the response
    gen = s.resolve_redirects(resp, req, yield_requests=True)
    
    new_req = next(gen)
    
    assert isinstance(new_req, PreparedRequest)
    assert new_req.url == "http://example.com/new"
    assert not s.send.called
