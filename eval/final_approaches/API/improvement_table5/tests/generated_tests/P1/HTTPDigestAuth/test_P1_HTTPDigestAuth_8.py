import pytest
import io
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_body_rewind():
    """
    Test that the request body is rewound (seek(pos)) before retrying after a 401 challenge.
    This ensures that streamed uploads or file bodies are resent correctly.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a seekable file-like body
    body_content = b"payload data"
    body = io.BytesIO(body_content)
    
    # Advance position to simulate partial read or previous attempt
    body.read(4) 
    initial_pos = body.tell() # Should be 4
    
    req = PreparedRequest()
    req.prepare(method="POST", url="http://example.com/upload", data=body)
    
    # Attach auth: this should record the current position (4)
    auth(req)
    
    # Read more to change position, simulating transmission
    body.read(4)
    assert body.tell() != initial_pos
    
    # Setup 401 response
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req
    r_401._content = b""
    r_401._content_consumed = True
    r_401.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    
    adapter_mock = Mock(spec=HTTPAdapter)
    adapter_mock.send.return_value = Response()
    adapter_mock.send.return_value._content = b""
    adapter_mock.send.return_value.history = []
    r_401.connection = adapter_mock
    
    # Trigger retry
    auth.handle_401(r_401)
    
    # Verify body was rewound to the position it was at when auth() was called
    assert body.tell() == initial_pos
    
    # Verify send was called
    assert adapter_mock.send.called