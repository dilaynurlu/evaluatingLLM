from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_simple_301():
    s = Session()
    s.send = Mock()
    
    # Original response
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/new"
    resp.url = "http://example.com/old"
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    # Next response
    next_resp = Response()
    next_resp.status_code = 200
    next_resp.url = "http://example.com/new"
    
    s.send.return_value = next_resp
    
    gen = s.resolve_redirects(resp, req)
    history = list(gen)
    
    assert len(history) == 1
    assert history[0] == next_resp
    s.send.assert_called_once()
