import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_sha256():
    """Test building digest header with SHA-256."""
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "test",
        "nonce": "123",
        "algorithm": "SHA-256"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    assert 'algorithm="SHA-256"' in header
