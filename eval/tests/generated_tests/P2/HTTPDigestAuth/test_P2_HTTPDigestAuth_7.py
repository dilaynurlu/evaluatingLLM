import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_retry_limit():
    """
    Test that handle_401 stops retrying after a certain number of 401 attempts
    to prevent infinite authentication loops.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = Mock(spec=requests.PreparedRequest)
    request.body = None
    
    # Initialize state
    auth(request)
    
    # Simulate having already hit the limit (set to 2)
    auth._thread_local.num_401_calls = 2
    
    response = Mock(spec=requests.Response)
    response.status_code = 401
    response.request = request
    # Valid digest header, but we've hit the limit
    response.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="nonce", qop="auth"'
    }
    
    # Act
    result = auth.handle_401(response)
    
    # Assert
    # It should return the original 401 response without attempting a retry
    assert result == response
    assert result.status_code == 401
    # Verify num_401_calls was reset to 1 (standard behavior when failing/giving up)
    assert auth._thread_local.num_401_calls == 1