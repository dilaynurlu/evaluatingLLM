import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_sha256():
    """
    Test Digest Auth with SHA-256 algorithm.
    Verifies that the algorithm parameter is correctly parsed from the challenge
    and included in the generated Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/")
    auth(request)
    
    response = Response()
    response.status_code = 401
    response.request = request
    # Challenge explicitly specifies SHA-256
    response.headers["www-authenticate"] = 'Digest realm="realm", nonce="abc", algorithm="SHA-256", qop="auth"'
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
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'response="' in auth_header
    # qop is auth, so nc and cnonce should be present
    assert 'nc=' in auth_header
    assert 'cnonce=' in auth_header