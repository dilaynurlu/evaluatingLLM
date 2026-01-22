from requests.auth import HTTPDigestAuth
import hashlib

def test_HTTPDigestAuth_SHA256():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "SHA-256"
    }
    header = auth.build_digest_header("GET", "http://example.com/")
    assert 'algorithm="SHA-256"' in header
    # Check if hash is correct length (64 chars hex)
    # response="..."
    import re
    match = re.search(r'response="([0-9a-f]+)"', header)
    assert match
    assert len(match.group(1)) == 64
