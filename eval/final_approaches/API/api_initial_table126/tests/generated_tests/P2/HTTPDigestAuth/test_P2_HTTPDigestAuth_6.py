import unittest.mock as mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_handle_401_success_retry():
    # Scenario: Received a valid 401 Digest challenge, should retry with Authorization header
    auth = HTTPDigestAuth("user", "pass")
    
    # 1. Prepare a mock request
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/protected")
    
    # 2. Prepare a response with 401 and Digest challenge
    response = Response()
    response.status_code = 401
    response.headers["www-authenticate"] = 'Digest realm="test", nonce="12345", qop="auth", algorithm="MD5"'
    response.request = request
    response._content = b""  # Avoid network I/O or stream consumption
    
    # 3. Mock the connection to intercept the retry
    mock_connection = mock.Mock()
    response.connection = mock_connection
    
    # The retry should return a new response (e.g., 200 OK)
    retry_response = Response()
    retry_response.status_code = 200
    retry_response.request = request.copy()
    mock_connection.send.return_value = retry_response
    
    # 4. Bind auth to request (initializes thread state)
    auth(request)
    
    # 5. Call handle_401 hook
    result = auth.handle_401(response)
    
    # Assertions
    assert result.status_code == 200
    assert mock_connection.send.called
    
    # Verify the retried request headers
    args, _ = mock_connection.send.call_args
    sent_request = args[0]
    
    assert "Authorization" in sent_request.headers
    auth_header = sent_request.headers["Authorization"]
    assert "Digest" in auth_header
    assert 'realm="test"' in auth_header
    assert 'nonce="12345"' in auth_header
    assert 'uri="/protected"' in auth_header