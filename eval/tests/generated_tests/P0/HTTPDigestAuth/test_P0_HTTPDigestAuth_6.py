import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_handle_401_retry_limit():
    """
    Test that handle_401 gives up if the number of 401 calls exceeds the limit (2).
    This prevents infinite loops if authentication fails repeatedly.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    response_401 = Mock()
    response_401.status_code = 401
    response_401.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n"'
    }
    response_401.is_redirect = False
    
    req = Mock()
    req.headers = {}
    # ensure body.tell() doesn't fail
    req.body = Mock()
    req.body.tell.return_value = 0
    
    # Init state
    auth(req)
    
    # Simulate that we have already tried twice (num_401_calls = 2)
    auth._thread_local.num_401_calls = 2
    
    # Act
    result = auth.handle_401(response_401)
    
    # Assert
    # Should return original response and not retry
    assert result is response_401
    # Should check if it resets the counter to 1 after giving up
    assert auth._thread_local.num_401_calls == 1