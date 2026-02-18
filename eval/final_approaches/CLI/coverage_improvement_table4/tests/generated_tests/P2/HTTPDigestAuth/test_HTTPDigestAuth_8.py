from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_handle_401_loop_prevention():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 2
    
    r = Mock()
    r.status_code = 401
    r.headers = {"www-authenticate": 'Digest realm="me", nonce="123"'}
    
    res = auth.handle_401(r)
    assert res is r
    assert auth._thread_local.num_401_calls == 1
