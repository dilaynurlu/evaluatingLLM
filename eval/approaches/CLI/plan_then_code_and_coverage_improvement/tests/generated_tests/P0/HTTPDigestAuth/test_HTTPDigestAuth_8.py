from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_8():
    # Test build_digest_header with MD5-SESS
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "MD5-SESS"
    }
    
    # We need to ensure cnonce generation is deterministic or we can't assert strict equality?
    # Or just check presence of fields.
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert 'algorithm="MD5-SESS"' in header
    # Check that HA1 calculation didn't crash
    assert "response=" in header
