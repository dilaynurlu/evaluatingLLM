import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_digest_auth_handle_redirect_resets_counter():
    """
    Test that handle_redirect resets the num_401_calls counter.
    This ensures that redirects don't exhaust the authentication retry limit erroneously.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock request and init
    request = Mock()
    request.headers = {}
    auth(request)
    
    # Simulate that we've used up calls
    auth._thread_local.num_401_calls = 10
    
    # Mock a redirect response
    response = Mock()
    response.is_redirect = True
    response.status_code = 302
    
    auth.handle_redirect(response)
    
    # Should be reset to 1
    assert auth._thread_local.num_401_calls == 1