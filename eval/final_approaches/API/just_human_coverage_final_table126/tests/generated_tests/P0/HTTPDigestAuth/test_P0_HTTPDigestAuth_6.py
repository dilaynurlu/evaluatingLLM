import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_redirect_reset():
    """
    Test that the 401 retry counter is reset when a redirect (3xx) occurs.
    This ensures that authentication retries are re-enabled after following a redirect.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize state
    auth.init_per_thread_state()
    
    # Manually exhaust the retry limit to simulate previous failures
    auth._thread_local.num_401_calls = 5
    
    # Create a redirect response
    redirect_res = requests.Response()
    redirect_res.status_code = 302
    redirect_res.headers["Location"] = "/new-location"
    
    # Call handle_redirect
    auth.handle_redirect(redirect_res)
    
    # Verify the counter is reset to 1
    assert auth._thread_local.num_401_calls == 1