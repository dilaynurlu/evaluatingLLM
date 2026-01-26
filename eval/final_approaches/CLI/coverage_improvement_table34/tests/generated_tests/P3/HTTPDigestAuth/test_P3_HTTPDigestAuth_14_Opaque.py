import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_build_digest_header_opaque():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "testrealm",
        "nonce": "testnonce",
        "qop": "auth",
        "opaque": "myopaque"
    }
    
    header = auth.build_digest_header("GET", "http://localhost/path")
    assert header.startswith("Digest ")
    assert 'opaque="myopaque"' in header
