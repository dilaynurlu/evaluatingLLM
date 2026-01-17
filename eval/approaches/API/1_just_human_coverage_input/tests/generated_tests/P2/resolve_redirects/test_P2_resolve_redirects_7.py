import pytest
from unittest.mock import MagicMock
from requests import Session, Request, Response
from requests.exceptions import UnrewindableBodyError
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_unrewindable_body_error():
    """
    Test that UnrewindableBodyError is raised if a redirect requires rewinding
    the request body (e.g., POST with stream), but the body object does not support seeking.
    """
    session = Session()
    
    # Create a non-seekable iterable body
    class NonSeekableBody:
        def __iter__(self):
            yield b'some_data'
        def read(self, size=None):
            return b'some_data'
        # No seek() method
    
    body_data = NonSeekableBody()
    
    # Prepare request
    # Note: Requests normally handles iterables by chunking, but we manually verify logic here.
    req = Request('POST', 'http://example.com/upload', data=body_data).prepare()
    
    # Force _body_position to be set (simulating it was recorded at start of request)
    # This signals that we *want* to rewind.
    req._body_position = 0
    
    # Create a redirect response that preserves method (307)
    resp = Response()
    resp.status_code = 307
    resp.url = 'http://example.com/upload'
    resp.headers = CaseInsensitiveDict({'Location': 'http://example.com/retry'})
    resp.raw = MagicMock()
    
    # Consuming the generator should trigger the rewind attempt and fail
    with pytest.raises(UnrewindableBodyError) as excinfo:
        # We must consume the generator to trigger execution
        next(session.resolve_redirects(resp, req))
        
    assert "Unable to rewind request body" in str(excinfo.value)