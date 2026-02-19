import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import UnrewindableBodyError

def test_resolve_redirects_unrewindable_body_error():
    """
    Test behavior when a request body cannot be rewound during a redirect (307/308).
    Should raise UnrewindableBodyError.
    """
    session = Session()
    
    # Prepare a request with a body
    req = Request('POST', 'http://example.com/upload', data=b'stream_data').prepare()
    
    # Simulate a stream that has been read and cannot be seeked/rewound.
    # Setting _body_position to object() simulates a failed tell() during preparation.
    req._body_position = object()
    # Content-Length header is present, triggering the rewind check
    req.headers['Content-Length'] = '11'
    
    # Response triggering a 307 redirect (must preserve body)
    resp_redirect = Response()
    resp_redirect.status_code = 307
    resp_redirect.headers['Location'] = 'http://example.com/upload_retry'
    resp_redirect.url = 'http://example.com/upload'
    resp_redirect.request = req
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = Mock()

    # resolve_redirects should attempt to rewind, fail, and raise UnrewindableBodyError
    with pytest.raises(UnrewindableBodyError) as excinfo:
        gen = session.resolve_redirects(resp_redirect, req)
        next(gen)
    
    assert "Unable to rewind request body" in str(excinfo.value)