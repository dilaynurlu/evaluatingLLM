import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import UnrewindableBodyError

class UnseekableBody:
    """A mock body that has a tell() method but fails or lacks seek()."""
    def __iter__(self):
        yield b"data"
    
    def tell(self):
        # Having tell() causes requests to record _body_position
        return 0
    
    # Missing seek() causes rewind_body to raise UnrewindableBodyError 
    # (or fails inside rewind_body logic)

def test_resolve_redirects_unrewindable_body_error():
    """
    Test that UnrewindableBodyError is raised if a request body cannot be 
    rewound (e.g., streamed body) during a 307 redirect which requires body preservation.
    """
    session = Session()
    
    # Create request with unseekable body
    req = Request('POST', 'http://example.com/upload', data=UnseekableBody())
    prep_req = session.prepare_request(req)
    
    # Verify precondition: _body_position was set because tell() exists
    assert prep_req._body_position == 0
    # Verify precondition: Transfer-Encoding is chunked because no len()
    assert prep_req.headers.get('Transfer-Encoding') == 'chunked'
    
    resp = Response()
    resp.status_code = 307 # Must be 307/308 to trigger body rewind
    resp.url = 'http://example.com/upload'
    resp.headers['Location'] = '/upload_v2'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Iterating should trigger rewind_body() which fails
    gen = session.resolve_redirects(resp, prep_req)
    
    with pytest.raises(UnrewindableBodyError):
        next(gen)
        
    # Verify connection was released despite error
    resp.raw.release_conn.assert_called()