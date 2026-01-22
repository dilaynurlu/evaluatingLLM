from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_opaque():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "r",
        "nonce": "n",
        "opaque": "myopaque"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    assert "opaque=\"myopaque\"" in header

