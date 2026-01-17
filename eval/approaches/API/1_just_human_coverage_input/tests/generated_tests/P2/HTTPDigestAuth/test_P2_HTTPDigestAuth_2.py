import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import Request, Response

def test_digest_auth_sha256_algorithm_support():
    """
    Test Digest Authentication using SHA-256 algorithm.
    Verifies that the algorithm parameter from the challenge is respected
    and echoed back in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.org/api").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.url = "http://example.org/api"
    response.request = req
    # Challenge specifying SHA-256
    response.headers["www-authenticate"] = (
        'Digest realm="secure_realm", nonce="abcde", qop="auth", algorithm="SHA-256"'
    )
    response._content = b""
    response.raw = Mock()
    
    mock_connection = Mock()
    response.connection = mock_connection
    mock_connection.send.return_value = Response() # Return empty success response
    
    auth.handle_401(response)
    
    assert mock_connection.send.called
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # Verify algorithm is set to SHA-256 in the response header
    assert 'algorithm="SHA-256"' in auth_header
    assert 'realm="secure_realm"' in auth_header