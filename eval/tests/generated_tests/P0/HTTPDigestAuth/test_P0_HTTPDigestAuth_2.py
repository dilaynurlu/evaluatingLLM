import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication using the SHA-256 algorithm.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Setup request and 401 response
    request = requests.Request("GET", "http://example.com/api").prepare()
    
    response_401 = requests.Response()
    response_401.status_code = 401
    response_401.headers["www-authenticate"] = (
        'Digest realm="SHA256Realm", nonce="randomnonce", '
        'qop="auth", algorithm="SHA-256"'
    )
    response_401.request = request
    response_401._content = b""
    response_401.raw = Mock()
    
    # Mock connection
    mock_connection = Mock()
    mock_response_final = requests.Response()
    mock_response_final.status_code = 200
    mock_response_final.history = []
    mock_response_final.request = requests.PreparedRequest()
    mock_connection.send.return_value = mock_response_final
    response_401.connection = mock_connection
    
    # Initialize auth
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    # Execute
    auth.handle_401(response_401)
    
    # Verify Authorization header for SHA-256 specific attributes
    args, _ = mock_connection.send.call_args
    sent_headers = args[0].headers
    auth_header = sent_headers["Authorization"]
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'nonce="randomnonce"' in auth_header
    # The response hash length for SHA-256 (64 hex chars) is different from MD5 (32 hex chars), 
    # but exact hash verification is complex. We verify structure.
    assert 'response="' in auth_header