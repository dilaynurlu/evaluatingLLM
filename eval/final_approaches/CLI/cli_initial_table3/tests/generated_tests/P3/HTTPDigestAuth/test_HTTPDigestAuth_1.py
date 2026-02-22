import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_MD5():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "realm",
        "nonce": "nonce",
        "qop": "auth",
        "algorithm": "MD5"
    }
    
    header = auth.build_digest_header("GET", "http://example.com/path")
    assert "username=\"user\"" in header
    assert "realm=\"realm\"" in header
    assert "nonce=\"nonce\"" in header
    assert "uri=\"/path\"" in header
    assert "response=" in header
    assert "qop=\"auth\"" in header

