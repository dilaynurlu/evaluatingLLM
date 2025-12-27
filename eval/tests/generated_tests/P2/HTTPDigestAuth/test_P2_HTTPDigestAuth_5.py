import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_nonce_count_increment():
    """
    Test that the nonce count (nc) increments when the same nonce is used
    across multiple header build calls, and resets when the nonce changes.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Manually populate thread local state to simulate parsed challenge
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "static_nonce",
        "qop": "auth"
    }
    
    # First call: nc should be 1
    header1 = auth.build_digest_header("GET", "http://example.org/")
    assert "nc=00000001" in header1
    
    # Second call (same nonce): nc should increment to 2
    header2 = auth.build_digest_header("GET", "http://example.org/")
    assert "nc=00000002" in header2
    
    # Change nonce
    auth._thread_local.chal["nonce"] = "new_nonce"
    
    # Third call (new nonce): nc should reset to 1
    header3 = auth.build_digest_header("GET", "http://example.org/")
    assert "nc=00000001" in header3