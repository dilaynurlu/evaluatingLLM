import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_build_digest_header_sha256():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "algorithm": "SHA-256",
        "qop": "auth"
    }
    auth._thread_local.nonce_count = 0
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    
    assert 'algorithm="SHA-256"' in header
    assert 'response="' in header
