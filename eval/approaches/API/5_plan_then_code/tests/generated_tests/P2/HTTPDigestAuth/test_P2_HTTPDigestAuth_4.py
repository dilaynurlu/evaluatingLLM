import pytest
import requests
from requests.auth import HTTPDigestAuth

def test_http_digest_auth_nonce_increment():
    """
    Test that the nonce count (nc) increments when the same nonce is reused
    across multiple requests (simulated by setting thread local state).
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Manually set the state to simulate a previous successful authentication
    # with a specific nonce.
    nonce = "reused_nonce"
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": nonce,
        "qop": "auth"
    }
    auth._thread_local.last_nonce = nonce
    auth._thread_local.nonce_count = 15  # Previous count was 15
    
    # Generate the header directly
    # This simulates a preemptive auth call or a subsequent request logic
    # that calls build_digest_header.
    header = auth.build_digest_header("GET", "http://example.com/")
    
    # Expect count to increment to 16 (hex 10)
    assert 'nc=00000010' in header
    assert 'nonce="reused_nonce"' in header
    
    # Ensure internal state was updated
    assert auth._thread_local.nonce_count == 16
    assert auth._thread_local.last_nonce == nonce