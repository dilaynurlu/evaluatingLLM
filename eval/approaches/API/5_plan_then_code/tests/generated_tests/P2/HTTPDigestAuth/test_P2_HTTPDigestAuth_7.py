import pytest
import requests
import io
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_body_rewind():
    """
    Test that the request body is rewound (seek(pos)) before retrying authentication.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a request with a file-like body
    body_data = b"abcdefg"
    body = io.BytesIO(body_data)
    
    req = requests.Request("POST", "http://example.com", data=body).prepare()
    
    # Simulate reading part of the body (as happens during sending)
    req.body.read(3)
    current_pos = req.body.tell()
    assert current_pos == 3
    
    # auth(req) records the current position (which should be start if called before send, 
    # but here we simulate the state where pos was recorded at start)
    # Re-create fresh body behavior for the test setup logic
    body.seek(0)
    auth(req) # records pos=0
    
    # Now simulate the body being consumed by the network send
    req.body.read(7)
    assert req.body.tell() == 7
    
    resp = requests.Response()
    resp.status_code = 401
    resp.request = req
    resp.headers = {"www-authenticate": 'Digest realm="r", nonce="n", qop="auth"'}
    resp._content = b""
    
    resp.connection = Mock()
    resp.raw = Mock()
    resp.connection.send.return_value = requests.Response()
    
    # Handle 401 should rewind body to pos (0)
    auth.handle_401(resp)
    
    # Verify body position is back to 0
    assert req.body.tell() == 0
    
    # Verify the body sent in the retry is correct
    sent_req = resp.connection.send.call_args[0][0]
    assert sent_req.body.read() == b"abcdefg"