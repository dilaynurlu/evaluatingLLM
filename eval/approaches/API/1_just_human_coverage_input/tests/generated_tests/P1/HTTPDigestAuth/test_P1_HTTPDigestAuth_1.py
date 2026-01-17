import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_md5_standard():
    """
    Test standard MD5 Digest Authentication with 'auth' QOP.
    Verifies that the Authorization header is correctly constructed with all required fields.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Prepare a request
    url = "http://example.org/resource"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    
    # Simulate a 401 Unauthorized response with Digest challenge
    resp = Response()
    resp.status_code = 401
    resp.headers["www-authenticate"] = 'Digest realm="testrealm", nonce="testnonce", algorithm="MD5", qop="auth", opaque="opaque-data"'
    resp.request = req
    resp._content = b""  # Empty content to prevent stream consumption issues
    
    # Mock the connection to capture the retried request
    mock_connection = Mock()
    success_response = Response()
    success_response.status_code = 200
    mock_connection.send.return_value = success_response
    resp.connection = mock_connection
    
    # Register hooks and initialize state
    auth(req)
    
    # Use patch to make cnonce and randomness deterministic
    # os.urandom returns 8 bytes, time.ctime returns a string
    with patch("os.urandom", return_value=b"\x01\x02\x03\x04\x05\x06\x07\x08"), \
         patch("time.ctime", return_value="Mon Jan 01 00:00:00 2000"):
        
        result = auth.handle_401(resp)
        
    # Assertions
    assert result == success_response
    assert mock_connection.send.called
    
    # Extract the retried request
    retry_req = mock_connection.send.call_args[0][0]
    auth_header = retry_req.headers.get("Authorization")
    
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Parse the header components
    # Header format example: Digest username="user", realm="...", ...
    params = {}
    parts = auth_header[7:].split(", ")
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            params[key] = value.strip('"')

    assert params["username"] == "user"
    assert params["realm"] == "testrealm"
    assert params["nonce"] == "testnonce"
    assert params["uri"] == "/resource"
    assert params["qop"] == "auth"
    assert params["nc"] == "00000001"
    assert params["opaque"] == "opaque-data"
    assert params["algorithm"] == "MD5"
    assert "response" in params
    assert "cnonce" in params