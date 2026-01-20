from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_method_preserve_307():
    s = Session()
    s.send = Mock()
    
    resp = Response()
    resp.status_code = 307
    resp.headers["Location"] = "/new"
    resp.url = "http://example.com/old"
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "POST"
    req.headers = {"Content-Length": "0"}
    req._cookies = RequestsCookieJar()
    req.body = Mock() # mock body to avoid unrewindable error
    req.body.seek = Mock()
    req._body_position = 0
    
    next_resp = Response()
    next_resp.status_code = 200
    s.send.return_value = next_resp
    
    list(s.resolve_redirects(resp, req))
    
    args, _ = s.send.call_args
    sent_req = args[0]
    assert sent_req.method == "POST"
