import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_build_digest_header_opaque():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "opaque": "opaque_data",
        "qop": "auth"
    }
    auth._thread_local.nonce_count = 0
    
    header = auth.build_digest_header("GET", "http://example.com/")
    
    assert 'opaque="opaque_data"' in header
