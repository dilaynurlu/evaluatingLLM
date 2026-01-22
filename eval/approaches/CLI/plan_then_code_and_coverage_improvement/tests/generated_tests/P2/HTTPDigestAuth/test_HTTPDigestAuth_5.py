from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_md5():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "MD5"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="realm"' in header
    assert 'nonce="nonce"' in header
    assert 'uri="/path"' in header
    assert 'response="' in header
    assert 'algorithm="MD5"' in header
