from unittest.mock import Mock, ANY
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_fragment():
    session = Session()
    
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "/new"}) # No fragment in new
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    resp.raw.stream.return_value = [b""]
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.com/old#frag"
    req.headers = CaseInsensitiveDict({})
    req._cookies = RequestsCookieJar()
    
    session.send = Mock(return_value=Response())
    
    list(session.resolve_redirects(resp, req))
    
    assert session.send.call_args[0][0].url == "http://example.com/new#frag"