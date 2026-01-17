import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_query_params():
    """
    Test Digest Auth header generation when URL contains query parameters.
    Verifies that the 'uri' directive in the Authorization header includes the query string.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    # URL with query parameters
    request.prepare(method="GET", url="http://example.com/path?foo=bar&baz=1")
    auth(request)
    
    response = Response()
    response.status_code = 401
    response.request = request
    response.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", qop="auth"'
    response._content = b""
    response.raw = Mock()
    del response.raw._original_response

    response.connection = Mock()
    mock_sent_response = Response()
    mock_sent_response.history = []
    response.connection.send.return_value = mock_sent_response

    auth.handle_401(response)
    
    assert response.connection.send.called
    sent_request = response.connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # Verify uri includes query
    assert 'uri="/path?foo=bar&baz=1"' in auth_header