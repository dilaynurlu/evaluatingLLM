import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_http_digest_auth_redirect_reset():
    """
    Test that handle_redirect resets the num_401_calls counter.
    This ensures that after a redirect, a new authentication flow can start fresh.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize state
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 10  # Simulate exhaustion
    
    resp = Mock(spec=Response)
    resp.is_redirect = True
    
    auth.handle_redirect(resp)
    
    assert auth._thread_local.num_401_calls == 1