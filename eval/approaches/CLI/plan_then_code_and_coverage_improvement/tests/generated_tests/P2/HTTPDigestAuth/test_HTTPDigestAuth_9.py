from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_call_uses_last_nonce():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.last_nonce = "prev_nonce"
    auth._thread_local.chal = {"realm": "r", "nonce": "prev_nonce", "qop": "auth"}
    
    r = Mock()
    r.headers = {}
    r.method = "GET"
    r.url = "http://example.com"
    r.body = None
    
    auth(r)
    
    assert "Authorization" in r.headers
    assert 'nonce="prev_nonce"' in r.headers["Authorization"]
