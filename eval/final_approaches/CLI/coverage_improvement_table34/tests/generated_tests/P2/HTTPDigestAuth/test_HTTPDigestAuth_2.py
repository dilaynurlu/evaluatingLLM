from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_handle_401_ignore_200():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Mock()
    r.status_code = 200
    
    res = auth.handle_401(r)
    assert res is r
    assert auth._thread_local.num_401_calls == 1
