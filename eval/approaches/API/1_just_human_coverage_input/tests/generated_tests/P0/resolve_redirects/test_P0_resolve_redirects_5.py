import pytest
from unittest.mock import Mock
from requests import Session, Request, Response
from requests.exceptions import UnrewindableBodyError

def test_resolve_redirects_unrewindable_body_error():
    """
    Test that UnrewindableBodyError is raised when attempting to redirect 
    a POST request with a streamed body that cannot be rewound.
    """
    session = Session()
    
    # Create a generator for the body (not rewindable)
    def body_generator():
        yield b"chunk1"
        yield b"chunk2"
        
    req = Request('POST', 'http://example.com/upload', data=body_generator())
    prep_req = req.prepare()
    
    # Manually simulate a failed tell() during preparation or a non-seekable stream.
    # requests sets _body_position to object() if tell() fails but it wants to mark it "potentially" rewindable to check later.
    # If _body_position is not None, resolve_redirects attempts to rewind.
    prep_req._body_position = object()
    
    # Response is 307 Temporary Redirect (preserves method/body)
    resp = Response()
    resp.status_code = 307
    resp.url = 'http://example.com/upload'
    resp.headers['Location'] = '/upload-retry'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    
    # Ensure headers trigger the rewind check
    prep_req.headers['Transfer-Encoding'] = 'chunked'
    
    # Execute
    gen = session.resolve_redirects(resp, prep_req)
    
    # Should raise UnrewindableBodyError because rewind_body fails on the generator
    with pytest.raises(UnrewindableBodyError) as excinfo:
        next(gen)
        
    assert "Unable to rewind request body" in str(excinfo.value)