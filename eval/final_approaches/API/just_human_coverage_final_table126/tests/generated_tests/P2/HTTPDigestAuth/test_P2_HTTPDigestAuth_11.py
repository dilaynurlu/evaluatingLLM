import threading
from requests.auth import HTTPDigestAuth

def test_build_digest_header_qop_selection():
    # Scenario: Server sends multiple QOP options, client prefers 'auth'
    auth = HTTPDigestAuth("user", "pass")
    
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "test",
        "nonce": "nonce",
        # List of options: auth-int, auth, etc.
        "qop": "auth-int,auth",
        "algorithm": "MD5"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    
    # Client should select "auth" and include it in the header
    assert 'qop="auth"' in header
    # Should not be auth-int
    assert 'qop="auth-int"' not in header