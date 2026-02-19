import unittest.mock as mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_handle_401_ignores_non_digest():
    # Scenario: Received a 401 with Basic auth challenge, DigestAuth should ignore it
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/basic")
    
    response = Response()
    response.status_code = 401
    response.headers["www-authenticate"] = 'Basic realm="test"'
    response.request = request
    response._content = b""
    
    mock_connection = mock.Mock()
    response.connection = mock_connection
    
    auth(request)
    
    # Call handle_401
    result = auth.handle_401(response)
    
    # Should return the original 401 response without retrying
    assert result is response
    assert not mock_connection.send.called
    assert result.status_code == 401