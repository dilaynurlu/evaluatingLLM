import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_nonce_count_increment():
    """
    Test that the nonce count (nc) increments when the same nonce is reused across requests
    (Preemptive authentication scenario).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # --- Step 1: Initial Handshake (First Request) ---
    req1 = requests.Request("GET", "http://example.com/r1").prepare()
    res1 = requests.Response()
    res1.status_code = 401
    res1.headers["www-authenticate"] = 'Digest realm="R", nonce="static_nonce", qop="auth"'
    res1.request = req1
    res1._content = b""
    res1.raw = Mock()
    
    mock_conn = Mock()
    res_success = requests.Response()
    res_success.status_code = 200
    res_success.history = []
    res_success.request = requests.PreparedRequest()
    mock_conn.send.return_value = res_success
    res1.connection = mock_conn
    
    # Process first 401
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    auth.handle_401(res1)
    
    # Verify first nc is 1
    req1_retry = mock_conn.send.call_args[0][0]
    assert 'nc=00000001' in req1_retry.headers["Authorization"]
    assert 'nonce="static_nonce"' in req1_retry.headers["Authorization"]
    
    # --- Step 2: Second Request (Preemptive Auth) ---
    # Create a new request object
    req2 = requests.Request("GET", "http://example.com/r2").prepare()
    
    # auth(req2) initializes state for the new request, resets num_401_calls,
    # but preserves thread-local challenge state (last_nonce, chal).
    # Since last_nonce matches "static_nonce", it adds header immediately.
    auth(req2)
    
    # Verify the header was added preemptively
    auth_header = req2.headers.get("Authorization")
    assert auth_header is not None
    assert 'nonce="static_nonce"' in auth_header
    
    # Critical Check: nc should be 2 because we are reusing the nonce
    assert 'nc=00000002' in auth_header