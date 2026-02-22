from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_4():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Mock()
    r.status_code = 200
    
    result = auth.handle_401(r)
    assert result == r
