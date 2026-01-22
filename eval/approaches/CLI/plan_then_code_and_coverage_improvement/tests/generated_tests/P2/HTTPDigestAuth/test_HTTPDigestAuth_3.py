from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_handle_401_no_digest():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Mock()
    r.status_code = 401
    r.headers = {"www-authenticate": "Basic realm=foo"}
    r.request.body = None
    
    res = auth.handle_401(r)
    assert res is r
    assert auth._thread_local.num_401_calls == 1
