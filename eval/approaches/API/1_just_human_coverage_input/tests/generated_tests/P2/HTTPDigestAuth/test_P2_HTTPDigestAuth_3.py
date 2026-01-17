import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import Request, Response

def test_digest_auth_legacy_no_qop():
    """
    Test Digest Authentication when the server provides no QOP (Quality of Protection).
    Verifies that the generated header omits qop, nc, and cnonce fields,
    conforming to RFC 2069 backward compatibility.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.org/legacy").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.url = "http://example.org/legacy"
    response.request = req
    # Challenge without qop
    response.headers["www-authenticate"] = 'Digest realm="legacy", nonce="54321"'
    response._content = b""
    response.raw = Mock()
    
    mock_connection = Mock()
    response.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    auth.handle_401(response)
    
    assert mock_connection.send.called
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # Assert fields that should NOT be present when qop is missing
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header
    
    # Assert basic fields are present
    assert 'username="user"' in auth_header
    assert 'realm="legacy"' in auth_header
    assert 'nonce="54321"' in auth_header
    assert 'response="' in auth_header