import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_redirect():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 5
    
    r = Mock()
    r.is_redirect = True
    
    auth.handle_redirect(r)
    
    assert auth._thread_local.num_401_calls == 1
