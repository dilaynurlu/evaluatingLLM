import pytest
import requests
import io
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_body_rewind():
    """
    Test that the request body is rewound to the starting position before retrying
    the request upon a 401 challenge.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a request with a seekable file-like body
    body_content = b"test_body_content"
    body_stream = io.BytesIO(body_content)
    
    # Wrap in a PreparedRequest
    req = requests.Request("POST", "http://example.com/post", data=body_stream).prepare()
    
    # Register auth hook to save the initial body position
    # This is normally done by requests inside prepare_request or send
    auth(req) 
    
    # Simulate partial read (as if sent over network)
    req.body.read(5)
    assert req.body.tell() == 5
    
    # Create 401 Response
    res_401 = requests.Response()
    res_401.status_code = 401
    res_401.headers["www-authenticate"] = 'Digest realm="R", nonce="N", qop="auth"'
    res_401.request = req
    res_401._content = b""
    res_401.raw = Mock()
    
    mock_conn = Mock()
    res_success = requests.Response()
    res_success.status_code = 200
    res_success.history = []
    res_success.request = requests.PreparedRequest()
    mock_conn.send.return_value = res_success
    res_401.connection = mock_conn
    
    # Handle 401
    auth.handle_401(res_401)
    
    # Check that body was rewound. 
    # Since handle_401 calls r.request.body.seek(pos), and pos was 0 (from auth(req) call)
    # The retried request should have body at position 0.
    # Note: requests.request.copy() shares the body object reference for streams.
    
    # Verify seek was called on the body stream
    # Since we used a real BytesIO, we can check the position or wrap it.
    # The retried request uses the same body object.
    assert req.body.tell() == 0
    
    # Ensure the retried request was sent with the body
    retry_req = mock_conn.send.call_args[0][0]
    assert retry_req.body is body_stream