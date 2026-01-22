import unittest.mock as mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_handle_401_max_retries_exceeded():
    # Scenario: If num_401_calls reaches 2, stop retrying to prevent infinite loops
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/loop")
    
    response = Response()
    response.status_code = 401
    response.headers["www-authenticate"] = 'Digest realm="test", nonce="123"'
    response.request = request
    response._content = b""
    
    # Mock connection
    mock_connection = mock.Mock()
    response.connection = mock_connection
    
    # Initialize and manually set counter to limit
    auth(request)
    auth._thread_local.num_401_calls = 2
    
    result = auth.handle_401(response)
    
    # Should return original response and reset counter to 1
    assert result is response
    assert not mock_connection.send.called
    assert auth._thread_local.num_401_calls == 1