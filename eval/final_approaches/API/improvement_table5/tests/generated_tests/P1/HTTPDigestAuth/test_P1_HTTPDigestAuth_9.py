import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_digest_auth_redirect_reset():
    """
    Test that handle_redirect resets the num_401_calls counter.
    This is important so that redirects don't accidentally consume the retry limit.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize state
    req = PreparedRequest()
    req.prepare("GET", "http://example.com")
    auth(req)
    
    # Simulate that we have already used up retries (limit is < 2, so set to 2)
    auth._thread_local.num_401_calls = 2
    
    # Create a redirect response (302 Found)
    r_redirect = Response()
    r_redirect.status_code = 302
    r_redirect.headers["Location"] = "/new"
    r_redirect.request = req
    
    # Call handle_redirect
    auth.handle_redirect(r_redirect)
    
    # Assert counter is reset to 1
    assert auth._thread_local.num_401_calls == 1