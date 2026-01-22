from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_3():
    # build_digest_header with MD5
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    # Mock challenge
    auth._thread_local.chal = {
        "realm": "me@kennethreitz.com",
        "nonce": "e30533031024505315354",
        "qop": "auth",
        "algorithm": "MD5"
    }
    header = auth.build_digest_header("GET", "http://example.com/")
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="me@kennethreitz.com"' in header
    assert 'nonce="e30533031024505315354"' in header
    assert 'algorithm="MD5"' in header
