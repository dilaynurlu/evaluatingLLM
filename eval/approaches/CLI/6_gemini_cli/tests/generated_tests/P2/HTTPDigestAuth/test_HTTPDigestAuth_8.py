import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_nonce_count():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth"
    }
    auth._thread_local.chal = chal
    
    # First call
    auth.build_digest_header("GET", "http://example.com/")
    count1 = auth._thread_local.nonce_count
    assert count1 == 1
    
    # Second call, same nonce
    auth.build_digest_header("GET", "http://example.com/")
    count2 = auth._thread_local.nonce_count
    assert count2 == 2
    
    # New nonce
    auth._thread_local.chal["nonce"] = "newnonce"
    auth.build_digest_header("GET", "http://example.com/")
    count3 = auth._thread_local.nonce_count
    assert count3 == 1
