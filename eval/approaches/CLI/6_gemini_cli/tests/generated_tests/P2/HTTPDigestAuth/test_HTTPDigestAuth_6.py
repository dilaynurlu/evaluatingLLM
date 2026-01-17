import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_no_qop():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/")
    # if not qop: respdig = KD(HA1, f"{nonce}:{HA2}")
    assert "qop" not in header
    assert "nc=" not in header
    assert "cnonce=" not in header
