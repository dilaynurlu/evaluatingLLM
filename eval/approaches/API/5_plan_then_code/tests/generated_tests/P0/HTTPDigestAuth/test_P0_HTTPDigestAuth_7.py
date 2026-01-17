import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_handle_redirect_resets_counter():
    """
    Test that handle_redirect resets the per-thread 401 counter.
    This ensures that redirects do not consume the limited number of allowed 401 retries.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Manually initialize thread local storage since we aren't calling __call__ fully
    auth.init_per_thread_state()
    
    # Artificially exhaust the retry limit
    auth._thread_local.num_401_calls = 5
    
    # Create a redirect response
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "/new"
    
    # Verify precondition
    assert resp.is_redirect
    
    # Call handle_redirect
    auth.handle_redirect(resp)
    
    # Verify counter is reset to 1
    assert auth._thread_local.num_401_calls == 1