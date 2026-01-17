import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_no_qop_backward_compatibility():
    """
    Test Digest Authentication without 'qop' in the challenge (RFC 2069 compatibility).
    Verifies that the generated Authorization header does NOT contain qop, nc, or cnonce.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    resp = Response()
    resp.request = req
    resp.status_code = 401
    # Challenge without qop
    resp.headers["www-authenticate"] = 'Digest realm="me", nonce="abc"'
    resp._content = b""
    resp.raw = Mock()
    
    mock_send = Mock()
    mock_send.return_value = Response()
    resp.connection = Mock()
    resp.connection.send = mock_send

    auth.handle_401(resp)
    
    assert mock_send.called
    auth_header = mock_send.call_args[0][0].headers["Authorization"]
    
    assert "Digest " in auth_header
    assert 'nonce="abc"' in auth_header
    # Ensure qop-related fields are absent
    assert "qop=" not in auth_header
    assert "nc=" not in auth_header
    assert "cnonce=" not in auth_header