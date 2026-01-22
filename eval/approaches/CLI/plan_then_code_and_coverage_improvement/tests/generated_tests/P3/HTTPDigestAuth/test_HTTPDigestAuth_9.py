from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_MD5_SESS():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "MD5-SESS"
    }
    header = auth.build_digest_header("GET", "http://example.com/")
    # Coverage for if _algorithm == "MD5-SESS": HA1 = ...
    assert 'algorithm="MD5-SESS"' in header
