import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_handle_redirect_reset():
    """
    Test that handle_redirect resets the num_401_calls counter.
    This ensures that after a successful auth and redirect, a subsequent 401 
    at the new location can still be handled.
    """
    auth = HTTPDigestAuth("user", "pass")
    request = Request("GET", "http://example.com/").prepare()
    auth(request)
    
    # Simulate that we've already consumed 1 auth attempt
    auth._thread_local.num_401_calls = 2
    
    # Create a redirect response
    # is_redirect depends on status code and Location header
    r_redirect = Response()
    r_redirect.status_code = 302
    r_redirect.headers["location"] = "http://example.com/new"
    r_redirect.request = request
    
    auth.handle_redirect(r_redirect)
    
    # Counter should be reset to 1
    assert auth._thread_local.num_401_calls == 1