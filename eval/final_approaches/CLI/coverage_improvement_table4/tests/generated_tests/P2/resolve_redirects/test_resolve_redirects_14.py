from unittest.mock import Mock, ANY
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_303_see_other():
    session = Session()
    
    resp = Response()
    resp.status_code = 303
    resp.headers = CaseInsensitiveDict({"Location": "/new"})
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    resp.raw.stream.return_value = [b""]
    
    req = PreparedRequest()
    req.method = "POST"
    req.url = "http://example.com/old"
    req.headers = CaseInsensitiveDict({"Content-Type": "x"})
    req.body = "data"
    req._cookies = RequestsCookieJar()
    
    session.send = Mock(return_value=Response())
    
    list(session.resolve_redirects(resp, req))
    
    new_req = session.send.call_args[0][0]
    # 303 should convert to GET and drop body
    assert new_req.method == "GET"
    assert new_req.body is None
    assert "Content-Type" not in new_req.headers
