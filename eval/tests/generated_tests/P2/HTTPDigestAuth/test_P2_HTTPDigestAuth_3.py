import threading
from requests.auth import HTTPDigestAuth

def test_build_digest_header_sha512():
    # Scenario: Verify correct Authorization header generation for SHA-512 algorithm
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize state
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "secure-realm",
        "nonce": "randomnonce",
        "qop": "auth",
        "algorithm": "SHA-512"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    
    assert header.startswith("Digest ")
    assert 'algorithm="SHA-512"' in header
    assert 'uri="/"' in header
    assert 'response="' in header