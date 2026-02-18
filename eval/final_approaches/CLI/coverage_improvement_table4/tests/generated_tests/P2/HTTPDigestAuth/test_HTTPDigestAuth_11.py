from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_md5_sess():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "MD5-SESS"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert 'algorithm="MD5-SESS"' in header
