import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_no_qop():
    """
    Test Digest Auth behavior when 'qop' is missing in the challenge (RFC 2069 compatibility).
    Verifies that cnonce and nc fields are NOT added to the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/old-server")
    auth(request)
    
    response = Response()
    response.status_code = 401
    response.request = request
    # Challenge without qop
    response.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce123"'
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
    
    # Should contain basic fields
    assert 'username="user"' in auth_header
    assert 'realm="realm"' in auth_header
    assert 'nonce="nonce123"' in auth_header
    assert 'response="' in auth_header
    
    # Should NOT contain qop-specific fields
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header