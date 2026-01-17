import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_http_digest_auth_handle_401_md5_success():
    """
    Test handling of a 401 response with a standard MD5 Digest challenge.
    Verifies that a new request is sent with a correctly formatted Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Setup a real PreparedRequest
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.org/resource"
    req.headers = {}
    req.hooks = {"response": []}
    
    # Initialize auth state (hooks, thread local)
    auth(req)
    
    # Setup the 401 Response
    resp = Mock(spec=Response)
    resp.request = req
    resp.status_code = 401
    resp.headers = {
        "www-authenticate": 'Digest realm="myrealm", nonce="nonce123", qop="auth", algorithm="MD5"'
    }
    resp.content = b""
    resp.raw = Mock()
    resp.raw._original_response = None  # Prevent cookie extraction logic
    resp.is_redirect = False
    resp.connection = Mock()
    
    # Mock the return value of the retried request
    retry_resp = Mock(spec=Response)
    retry_resp.history = []
    retry_resp.request = None
    resp.connection.send.return_value = retry_resp
    
    # Trigger handle_401
    result = auth.handle_401(resp)
    
    # Verify the retry occurred
    assert result == retry_resp
    assert resp.connection.send.called
    
    # Inspect the Authorization header in the retried request
    args, _ = resp.connection.send.call_args
    sent_request = args[0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Parse header to verify components
    # Header format: Digest username="...", realm="...", ...
    params = {}
    parts = auth_header[7:].split(",")
    for part in parts:
        key, value = part.strip().split("=", 1)
        params[key] = value.strip('"')

    assert params['username'] == "user"
    assert params['realm'] == "myrealm"
    assert params['nonce'] == "nonce123"
    assert params['uri'] == "/resource"
    assert params['algorithm'] == "MD5"
    assert params['qop'] == "auth"
    assert params['nc'] == "00000001"
    assert len(params['cnonce']) > 0
    assert len(params['response']) > 0