import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth

def test_request_body_rewind():
    """
    Test that if a request body stream supports tell/seek, 
    handle_401 rewinds it before retrying.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock a file-like body
    body_mock = Mock()
    body_mock.tell.return_value = 100
    
    request = Mock()
    request.body = body_mock
    request.headers = {}
    request.register_hook = Mock()
    
    # 1. Call auth(request) to save position
    auth(request)
    assert auth._thread_local.pos == 100
    
    # 2. Handle 401
    response = Mock()
    response.status_code = 401
    response.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n"'
    }
    response.request = request
    # Setup copy
    request.copy.return_value = Mock(headers={}, method="GET", url="http://a.com")
    response.connection.send.return_value = Mock(history=[])
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth.handle_401(response)
        
    # Assert seek was called with the saved position
    body_mock.seek.assert_called_with(100)