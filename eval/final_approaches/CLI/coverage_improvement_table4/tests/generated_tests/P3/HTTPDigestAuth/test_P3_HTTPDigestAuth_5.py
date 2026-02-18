import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_stop_loop():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 2 # Limit is 2
    
    r = Mock(spec=Response)
    r.status_code = 401
    r.headers = {"www-authenticate": 'Digest realm="me@test.com", nonce="nonce"'}
    r.request = Mock(spec=PreparedRequest)
    r.request.body = Mock()
    
    result = auth.handle_401(r)
    
    assert result == r
    assert auth._thread_local.num_401_calls == 1 # Resets to 1
