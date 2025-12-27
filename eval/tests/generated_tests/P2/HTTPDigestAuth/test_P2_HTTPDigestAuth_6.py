import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_handle_redirect_resets_counter():
    """
    Test that handle_redirect resets the num_401_calls counter.
    This ensures that redirects during the auth flow do not exhaust the retry limit.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Simulate that we have already tried once
    auth._thread_local.num_401_calls = 2
    
    # Mock a redirect response
    response = Mock(spec=requests.Response)
    response.is_redirect = True
    
    # Act
    auth.handle_redirect(response)
    
    # Assert
    assert auth._thread_local.num_401_calls == 1