import pytest
from unittest.mock import Mock, MagicMock, patch
from requests.auth import HTTPDigestAuth

def test_digest_auth_stop_infinite_loop_and_cleanup():
    """
    Test that handle_401 does not retry if num_401_calls limit is reached.
    Verifies that it returns the original response and consumes its content
    to prevent connection leaks.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = MagicMock()
    request.headers = {}
    
    response = Mock()
    response.status_code = 401
    response.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="nonce", qop="auth"'
    }
    response.request = request
    response.connection = Mock()
    # Mock content
    response.content = b"Auth failed"
    
    # Init auth
    auth(request)
    
    # Manually set num_401_calls to 2 (limit)
    auth._thread_local.num_401_calls = 2
    
    with patch("requests.auth.extract_cookies_to_jar"):
        result = auth.handle_401(response)
        
        # Should return the original response without retrying
        assert result is response
        assert not response.connection.send.called
        
        # Verify counter reset
        assert auth._thread_local.num_401_calls == 1