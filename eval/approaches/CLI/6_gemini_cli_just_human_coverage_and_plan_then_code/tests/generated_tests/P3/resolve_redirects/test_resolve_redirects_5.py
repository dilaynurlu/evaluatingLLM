from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_rewind_body():
    s = Session()
    s.send = Mock()
    
    resp = Response()
    resp.status_code = 307 # Use 307 to preserve body
    resp.headers["Location"] = "/new"
    resp.url = "http://example.com/old"
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "POST"
    req.headers = {"Content-Length": "5"}
    req._cookies = RequestsCookieJar()
    
    # Mock body with seek
    req.body = Mock()
    req._body_position = 0
    
    next_resp = Response()
    next_resp.status_code = 200
    s.send.return_value = next_resp
    
    list(s.resolve_redirects(resp, req))
    
    req.body.seek.assert_called_with(0)
