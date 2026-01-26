import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_handle_401_status_404():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Response()
    r.status_code = 404 # Not 401
    
    # Should reset num_401_calls and return response
    result = auth.handle_401(r)
    
    assert result == r
    assert auth._thread_local.num_401_calls == 1
