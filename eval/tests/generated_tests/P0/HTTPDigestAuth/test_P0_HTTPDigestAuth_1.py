import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock, MagicMock

def test_digest_auth_md5_success():
    """
    Test a basic successful Digest Authentication flow using MD5 algorithm.
    Verifies that the Authorization header is correctly constructed and the request is retried.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create the original request
    url = "http://example.com/sensitive"
    request = requests.Request("GET", url).prepare()
    
    # Create the 401 response from the server
    response_401 = requests.Response()
    response_401.status_code = 401
    # Standard Digest header
    response_401.headers["www-authenticate"] = (
        'Digest realm="TestRealm", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", '
        'qop="auth", opaque="5ccc069c403ebaf9f0171e9517f40e41", algorithm="MD5"'
    )
    response_401.request = request
    response_401._content = b""  # Empty content to avoid reading from raw
    response_401.raw = Mock()    # Mock raw to satisfy cookie extraction checks
    
    # Mock the connection object attached to the response
    # When handle_401 calls r.connection.send, it should return a success response
    mock_connection = Mock()
    response_success = requests.Response()
    response_success.status_code = 200
    response_success.history = [] # Initialize history list
    response_success.request = requests.PreparedRequest()
    
    # The send method returns the new response
    mock_connection.send.return_value = response_success
    response_401.connection = mock_connection
    
    # Initialize the auth state (usually done by __call__)
    auth.init_per_thread_state()
    # Ensure call counter is initialized
    auth._thread_local.num_401_calls = 1
    
    # Trigger the 401 handler
    result = auth.handle_401(response_401)
    
    # Verification
    assert result.status_code == 200
    assert mock_connection.send.call_count == 1
    
    # Inspect the request sent by connection.send
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    
    # Verify components of the Digest header
    assert 'username="user"' in auth_header
    assert 'realm="TestRealm"' in auth_header
    assert 'nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093"' in auth_header
    assert 'uri="/sensitive"' in auth_header
    assert 'algorithm="MD5"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert 'cnonce="' in auth_header
    assert 'opaque="5ccc069c403ebaf9f0171e9517f40e41"' in auth_header
    assert 'response="' in auth_header
    
    # Verify history is updated
    assert len(result.history) == 1
    assert result.history[0] == response_401