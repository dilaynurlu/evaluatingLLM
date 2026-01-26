import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_sha256():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "testrealm",
        "nonce": "testnonce",
        "qop": "auth",
        "algorithm": "SHA-256"
    }
    
    header = auth.build_digest_header("GET", "http://localhost/path")
    assert header.startswith("Digest ")
    assert 'algorithm="SHA-256"' in header
