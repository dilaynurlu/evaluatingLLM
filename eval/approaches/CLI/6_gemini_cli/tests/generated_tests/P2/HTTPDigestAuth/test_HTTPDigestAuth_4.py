import pytest
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
    # If algorithm is MD5-SESS, HA1 includes cnonce.
    # Code: if _algorithm == "MD5-SESS": HA1 = hash_utf8(f"{HA1}:{nonce}:{cnonce}")
    # Just checking it runs without error and produces header.
    assert header.startswith("Digest ")
