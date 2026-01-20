from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import UnrewindableBodyError
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_unrewindable():
    s = Session()
    s.send = Mock()
    
    resp = Response()
    resp.status_code = 307 # 307 preserves POST
    resp.headers["Location"] = "/new"
    resp.url = "http://example.com/old"
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "POST"
    req.headers = {"Content-Length": "5"}
    req._cookies = RequestsCookieJar()
    
    # Mock body WITHOUT seek, or with seek failing
    req.body = object() # No seek method
    req._body_position = 0
    
    try:
        next(s.resolve_redirects(resp, req))
    except UnrewindableBodyError:
        pass
    else:
        assert False, "Should have raised UnrewindableBodyError"
