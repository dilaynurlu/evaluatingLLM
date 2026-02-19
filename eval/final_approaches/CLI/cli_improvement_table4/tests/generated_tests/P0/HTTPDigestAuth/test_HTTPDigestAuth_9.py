from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_9():
    # Test build_digest_header with unknown/unsupported qop
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth-int", # Not supported by requests yet
        "algorithm": "MD5"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    # Should return None if it falls through to 'else'
    assert header is None
