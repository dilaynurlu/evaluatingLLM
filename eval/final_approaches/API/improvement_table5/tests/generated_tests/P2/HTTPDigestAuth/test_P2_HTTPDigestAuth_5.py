import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_preemptive_nonce_reuse():
    """
    Test preemptive authentication where a nonce is reused.
    Simulates a scenario where thread-local state is already populated from a previous
    successful auth, and verify the 'nonce_count' increments.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # 1. Manually populate thread-local state to simulate a previous 401 challenge
    auth.init_per_thread_state()
    auth._thread_local.init = True
    auth._thread_local.chal = {
        "realm": "realm", 
        "nonce": "reused_nonce", 
        "qop": "auth", 
        "algorithm": "MD5"
    }
    auth._thread_local.last_nonce = "reused_nonce"
    auth._thread_local.nonce_count = 1
    
    # 2. Prepare a new request
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/next_resource")
    
    # 3. Call auth() which checks _thread_local.last_nonce
    # Since last_nonce is set, it should preemptively add Authorization header
    auth(req)
    
    # 4. Verify Authorization header is present immediately
    auth_header = req.headers.get("Authorization")
    assert auth_header is not None
    assert 'Digest ' in auth_header
    assert 'nonce="reused_nonce"' in auth_header
    
    # 5. Verify nonce_count incremented (1 -> 2)
    # The NC value in header should be 00000002
    assert 'nc=00000002' in auth_header
    
    # Verify internal state updated
    assert auth._thread_local.nonce_count == 2