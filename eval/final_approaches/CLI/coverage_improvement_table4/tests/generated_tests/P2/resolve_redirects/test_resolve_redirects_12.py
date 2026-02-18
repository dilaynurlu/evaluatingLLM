from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import ChunkedEncodingError
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_chunked_error_suppressed():
    session = Session()
    
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "/new"})
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    resp.raw.headers = resp.headers
    
    def generate_error():
        raise ChunkedEncodingError("Connection broken")
        yield b""
    
    resp.raw.stream.return_value = generate_error()
    
    # Remove previous mock of content property if any
    # (Checking logic: resp.content accesses iter_content -> raw.stream)
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.com/old"
    req.headers = CaseInsensitiveDict({})
    req._cookies = RequestsCookieJar()
    
    session.send = Mock(return_value=Response())
    
    # Should not raise
    list(session.resolve_redirects(resp, req))
    
    # Verify raw.read called
    resp.raw.read.assert_called_with(decode_content=False)
