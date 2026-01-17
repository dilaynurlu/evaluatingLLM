from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_strip_headers():
    s = Session()
    s.send = Mock()
    
    resp = Response()
    resp.status_code = 302 # Found -> GET
    resp.headers["Location"] = "/new"
    resp.url = "http://example.com/old"
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "POST"
    req.headers = {"Content-Length": "100", "Content-Type": "text/plain", "Transfer-Encoding": "chunked", "X-Custom": "keep"}
    req._cookies = RequestsCookieJar()
    
    next_resp = Response()
    next_resp.status_code = 200
    s.send.return_value = next_resp
    
    list(s.resolve_redirects(resp, req))
    
    args, _ = s.send.call_args
    sent_req = args[0]
    assert sent_req.method == "GET"
    assert "Content-Length" not in sent_req.headers
    assert "Content-Type" not in sent_req.headers
    assert "Transfer-Encoding" not in sent_req.headers
    assert "X-Custom" in sent_req.headers
