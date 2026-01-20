import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_build_digest_header_md5():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Manually setup thread local state as if a 401 happened
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "algorithm": "MD5",
        "qop": "auth"
    }
    auth._thread_local.nonce_count = 0
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    
    assert header.startswith("Digest ")
    assert 'username="user"' in header
    assert 'realm="realm"' in header
    assert 'nonce="nonce"' in header
    assert 'uri="/path"' in header
    assert 'response="' in header
    assert 'algorithm="MD5"' in header
