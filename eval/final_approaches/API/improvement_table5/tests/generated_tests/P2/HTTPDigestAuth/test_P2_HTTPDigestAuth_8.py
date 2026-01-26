import pytest
import io
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_rewind_body():
    """
    Test that handle_401 rewinds the request body if possible.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # 1. Prepare request with a file-like body
    body_content = b"test body content"
    body_file = io.BytesIO(body_content)
    
    req = PreparedRequest()
    req.prepare(
        method="POST", 
        url="http://example.com/", 
        data=body_file
    )
    
    # 2. Attach auth (this saves body position, which is 0 currently)
    auth(req)
    
    # 3. Simulate reading part of the body (as if network sent it)
    req.body.read(5)
    assert req.body.tell() == 5
    
    # 4. Create 401 Response
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    handle_401_hook = req.hooks["response"][0]
    
    # 5. Trigger retry
    handle_401_hook(resp)
    
    # 6. Verify body was rewound to 0 (saved position)
    # The 'sent_request' in connection.send should have body at position 0
    # or the original req body should be reset.
    assert req.body.tell() == 0