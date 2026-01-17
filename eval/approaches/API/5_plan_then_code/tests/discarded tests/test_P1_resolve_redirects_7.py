import pytest
import io
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_rewind_body():
    """
    Test that if a request with a body is redirected (e.g. 307),
    the body is rewound (seek(0)) so it can be re-sent.
    """
    session = Session()
    
    # Create a file-like body
    body_content = b"test content"
    body = io.BytesIO(body_content)
    
    # We need to simulate that the body was read. Move position.
    body.read() 
    assert body.tell() == len(body_content)
    
    # Create request
    req = PreparedRequest()
    req.prepare(
        method="POST",
        url="http://example.com/post",
        data=body
    )
    
    # Manually set _body_position to 0 (start) as requests does during send()
    req._body_position = 0
    
    # 307 Redirect (Preserves method and body)
    resp = Response()
    resp.status_code = 307
    resp.headers["Location"] = "http://example.com/post_new"
    resp.url = "http://example.com/post"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    resp_200 = Response()
    resp_200.status_code = 200
    resp_200.url = "http://example.com/post_new"
    resp_200._content = b""
    resp_200._content_consumed = True
    
    session.send = Mock(return_value=resp_200)
    
    # We patch requests.sessions.rewind_body to verify it is called.
    # Alternatively, we can check if body.seek(0) happened.
    # Since 'rewind_body' is imported in the module, we patch it there.
    
    with patch("requests.sessions.rewind_body") as mock_rewind:
        list(session.resolve_redirects(resp, req))
        
        # Verify rewind_body was called with the prepared request
        assert mock_rewind.called
        args, _ = mock_rewind.call_args
        assert args[0].body == body
        
    # Also verify the logic that triggers it:
    # 1. req._body_position is not None
    # 2. Content-Length or Transfer-Encoding is present (prepare adds Content-Length for BytesIO)
    assert "Content-Length" in req.headers
    assert req._body_position is not None