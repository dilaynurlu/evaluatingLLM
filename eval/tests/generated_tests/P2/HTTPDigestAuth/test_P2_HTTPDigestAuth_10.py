import io
import unittest.mock as mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_handle_401_rewinds_body():
    # Scenario: When retrying, the request body stream must be rewound
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a request with a file-like body
    body_data = b"request body data"
    body = io.BytesIO(body_data)
    
    request = PreparedRequest()
    request.prepare(method="POST", url="http://example.com/post", data=body)
    
    # Simulate body having been read partially or fully
    body.read() 
    assert body.tell() == len(body_data)
    
    # Setup response
    response = Response()
    response.status_code = 401
    response.headers["www-authenticate"] = 'Digest realm="test", nonce="123", qop="auth"'
    response.request = request
    response._content = b""
    response.connection = mock.Mock()
    response.connection.send.return_value = Response()
    
    # Register auth (this records initial body position)
    # We need to ensure the initial position is recorded as 0 (start)
    body.seek(0)
    auth(request) 
    
    # Now advance body again to simulate transmission
    body.read()
    
    # Trigger retry
    auth.handle_401(response)
    
    # The body should have been rewound to 0 before the retry send
    # Note: Since we mock connection.send, the actual read happens inside send usually.
    # But handle_401 explicitly calls r.request.body.seek(pos).
    # We can check if seek(0) was called.
    
    # Since io.BytesIO.seek is a real method, we verify state or mock it.
    # Using a Mock wrap on BytesIO is cleaner to verify the call.
    # But checking the position after handle_401 returns (if mock_send reads it) is tricky.
    # Instead, let's verify that the position was reset at the moment of `send`.
    
    # However, since we mock send, we can inspect the body position of the request passed to send.
    args, _ = response.connection.send.call_args
    sent_req = args[0]
    
    # handle_401 seeks the body.
    # Since we didn't consume it inside the mock send, it should be at 0.
    assert sent_req.body.tell() == 0