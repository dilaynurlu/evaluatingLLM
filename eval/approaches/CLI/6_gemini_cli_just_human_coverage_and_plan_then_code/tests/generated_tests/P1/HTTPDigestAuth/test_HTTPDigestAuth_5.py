import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_ignore_200():
    auth = HTTPDigestAuth("user", "pass")
    
    r = Mock()
    r.status_code = 200
    
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    result = auth.handle_401(r)
    
    assert result == r # Should return original response
    assert auth._thread_local.num_401_calls == 1 # Should reset calls
