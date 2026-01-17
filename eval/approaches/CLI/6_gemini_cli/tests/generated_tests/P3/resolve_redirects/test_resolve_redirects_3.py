from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_relative_scheme():
    s = Session()
    s.send = Mock()
    
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "//example.com/new"
    resp.url = "http://example.com/old" # Scheme is http
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    next_resp = Response()
    next_resp.status_code = 200
    
    s.send.return_value = next_resp
    
    list(s.resolve_redirects(resp, req))
    
    args, _ = s.send.call_args
    sent_req = args[0]
    assert sent_req.url == "http://example.com/new"
