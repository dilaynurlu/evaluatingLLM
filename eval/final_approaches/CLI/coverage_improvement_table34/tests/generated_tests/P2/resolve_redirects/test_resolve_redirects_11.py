from unittest.mock import Mock
import pytest
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import UnrewindableBodyError
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_unrewindable_body():
    session = Session()
    
    resp = Response()
    resp.status_code = 307
    resp.headers = CaseInsensitiveDict({"Location": "/new"})
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    resp.raw.stream.return_value = [b""]
    
    req = PreparedRequest()
    req.method = "POST"
    req.url = "http://example.com/old"
    req.headers = CaseInsensitiveDict({"Content-Length": "100"})
    req._cookies = RequestsCookieJar()
    
    # To trigger rewind_body, we need _body_position set and CL/TE header
    req._body_position = 0 
    
    # To make rewind_body raise UnrewindableBodyError, make seek fail
    req.body = Mock()
    req.body.seek.side_effect = OSError("Seek failed")
    
    session.send = Mock(return_value=Response())
    
    with pytest.raises(UnrewindableBodyError):
        list(session.resolve_redirects(resp, req))
