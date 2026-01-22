from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_10():
    # Test build_digest_header with opaque
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "MD5",
        "opaque": "myopaquevalue"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert 'opaque="myopaquevalue"' in header
