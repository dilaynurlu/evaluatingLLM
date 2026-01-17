import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_digest_auth_handle_redirect_reset():
    """
    Test that handle_redirect resets the num_401_calls counter.
    """
    auth = HTTPDigestAuth("user", "pass")
    # Initialize state
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 10  # Arbitrary high number
    
    # Mock a response object that acts like a redirect
    response = Response()
    response.status_code = 302
    response.headers["Location"] = "/new-location"
    
    # Verify is_redirect is True (requests.models.Response logic relies on status code & location header)
    # Since we are using real Response object, status 302 + Location header makes is_redirect True.
    assert response.is_redirect
    
    auth.handle_redirect(response)
    
    assert auth._thread_local.num_401_calls == 1