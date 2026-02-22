import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_handle_redirect_reset():
    """
    Test that handle_redirect resets num_401_calls.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Simulate some previous calls
    auth._thread_local.num_401_calls = 5
    
    # Mock redirect response
    r = MagicMock(spec=Response)
    r.is_redirect = True
    
    auth.handle_redirect(r)
    
    assert auth._thread_local.num_401_calls == 1
