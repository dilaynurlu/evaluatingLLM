import threading
from requests.auth import HTTPDigestAuth

def test_build_digest_header_no_qop():
    # Scenario: Verify header generation when QOP is missing (RFC 2069 compatibility)
    auth = HTTPDigestAuth("user", "pass")
    
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "legacy-realm",
        "nonce": "legacy-nonce",
        # No qop, no algorithm (defaults to MD5)
    }
    
    header = auth.build_digest_header("GET", "http://example.com/legacy")
    
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="legacy-realm"' in header
    assert 'nonce="legacy-nonce"' in header
    assert 'uri="/legacy"' in header
    assert 'response="' in header
    
    # These fields should NOT be present when qop is missing
    assert 'qop=' not in header
    assert 'nc=' not in header
    assert 'cnonce=' not in header