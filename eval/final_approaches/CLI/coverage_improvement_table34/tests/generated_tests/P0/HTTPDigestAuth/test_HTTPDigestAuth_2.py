from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_2():
    # Test build_digest_header with SHA-256
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "SHA-256"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert "algorithm=\"SHA-256\"" in header
    # SHA-256 hash length is distinct (64 chars hex)
    # But response is calculated from H(A1) etc.
    # Just checking presence and lack of crash is good for P0.
    assert "response=" in header
