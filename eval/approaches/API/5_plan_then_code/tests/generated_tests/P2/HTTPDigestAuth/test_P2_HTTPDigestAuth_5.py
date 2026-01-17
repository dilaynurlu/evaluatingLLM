import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_handle_redirect_reset():
    """
    Test that handle_redirect resets the num_401_calls counter.
    This ensures that after a redirect, a new authentication challenge loop can start.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Simulate that we have already tried once
    auth._thread_local.num_401_calls = 2
    
    # Create a redirect response
    resp = requests.Response()
    resp.status_code = 302
    resp.headers["Location"] = "/new-location"
    
    # Call handle_redirect
    auth.handle_redirect(resp)
    
    # Verify counter is reset to 1
    assert auth._thread_local.num_401_calls == 1