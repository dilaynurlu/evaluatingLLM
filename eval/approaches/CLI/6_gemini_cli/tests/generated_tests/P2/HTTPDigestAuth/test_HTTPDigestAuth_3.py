import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_SHA512():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "SHA-512"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    assert 'algorithm="SHA-512"' in header
