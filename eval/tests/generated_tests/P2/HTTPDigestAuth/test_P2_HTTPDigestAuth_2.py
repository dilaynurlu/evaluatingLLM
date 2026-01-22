import threading
from requests.auth import HTTPDigestAuth

def test_build_digest_header_sha256():
    # Scenario: Verify correct Authorization header generation for SHA-256 algorithm
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize state
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "test",
        "nonce": "abc123nonce",
        "qop": "auth",
        "algorithm": "SHA-256"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/resource")
    
    assert header.startswith("Digest ")
    assert 'algorithm="SHA-256"' in header
    assert 'username="user"' in header
    assert 'realm="test"' in header
    assert 'uri="/resource"' in header
    # Ensure response field is present (length checks or content checks are hard due to hashing, but presence is key)
    assert 'response="' in header