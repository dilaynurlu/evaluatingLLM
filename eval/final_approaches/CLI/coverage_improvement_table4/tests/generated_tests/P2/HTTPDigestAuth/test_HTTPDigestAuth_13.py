from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_no_qop():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        # no qop
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    # If no qop, no cnonce/nc in header usually (RFC 2617 legacy mode)
    assert 'qop=' not in header
    assert 'cnonce=' not in header
    assert 'nc=' not in header
