import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_too_many():
    session = Session()
    session.max_redirects = 2
    
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "http://example.com/loop"})
    resp.url = "http://example.com/start"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    resp.raw.stream.return_value = [b""]
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.com/start"
    req.headers = CaseInsensitiveDict({})
    req._cookies = RequestsCookieJar()
    
    # Mock send to always return a redirect
    def side_effect(*args, **kwargs):
        r = Response()
        r.status_code = 301
        r.headers = CaseInsensitiveDict({"Location": "http://example.com/loop"})
        r.url = args[0].url
        r.raw = Mock()
        r.raw.headers = r.headers
        r.raw.stream.return_value = [b""]
        return r
    
    session.send = Mock(side_effect=side_effect)
    
    with pytest.raises(TooManyRedirects):
        list(session.resolve_redirects(resp, req))