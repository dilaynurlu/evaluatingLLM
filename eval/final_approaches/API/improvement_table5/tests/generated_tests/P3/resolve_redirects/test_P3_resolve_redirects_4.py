import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import UnrewindableBodyError
from unittest.mock import MagicMock

def test_resolve_redirects_308_preserves_method_and_body_rewind():
    """
    Refined test for 308 Permanent Redirect.
    Verifies:
    1. HTTP 308 acts like 307: Preserves method (POST) and body.
    2. The body stream is rewound (seek(0)) before re-sending.
    """
    session = Session()
    
    # Setup a mock file-like body that tracks seeking
    class MockBody:
        def __init__(self, data):
            self.data = data
            self.pos = 0
            self.seek_called = False
            
        def read(self, size=-1):
            return self.data
            
        def seek(self, pos, whence=0):
            self.seek_called = True
            self.pos = pos
            
        def tell(self):
            return self.pos

    body_content = b"important_data"
    mock_body = MockBody(body_content)
    
    req = Request("POST", "http://example.com/submit", data=mock_body).prepare()
    
    # 308 Response
    resp = Response()
    resp.request = req
    resp.url = "http://example.com/submit"
    resp.status_code = 308  # Permanent Redirect (RFC 7538)
    resp.headers["Location"] = "http://example.com/submit_perm"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Mock target response
    resp_target = Response()
    resp_target.status_code = 200
    session.send = MagicMock(return_value=resp_target)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Verify
    session.send.assert_called_once()
    sent_req = session.send.call_args[0][0]
    
    # 1. Method must remain POST for 308
    assert sent_req.method == "POST"
    
    # 2. Body must still be present
    assert sent_req.body == mock_body
    
    # 3. Rewind verification: assert seek(0) was called on the body
    assert mock_body.seek_called is True