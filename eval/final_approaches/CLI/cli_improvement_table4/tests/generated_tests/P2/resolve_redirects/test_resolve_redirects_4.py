from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_yield_requests():
    session = Session()
    
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "http://example.com/new"})
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    resp.raw.stream.return_value = [b""]
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.com/old"
    req.headers = CaseInsensitiveDict({})
    req._cookies = RequestsCookieJar()
    
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    item = next(gen)
    
    assert isinstance(item, PreparedRequest)
    assert item.url == "http://example.com/new"