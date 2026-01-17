import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_no_qop():
    """
    Test Digest Authentication when 'qop' is missing from the challenge (RFC 2069 compatibility).
    Verifies that qop, nc, and cnonce are NOT present in the generated header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    url = "http://example.org/legacy"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    
    resp = Response()
    resp.status_code = 401
    # Challenge WITHOUT qop
    resp.headers["www-authenticate"] = 'Digest realm="legacy", nonce="legacy_nonce"'
    resp.request = req
    resp._content = b""
    
    mock_connection = Mock()
    mock_connection.send.return_value = Response()
    resp.connection = mock_connection
    
    auth(req)
    
    auth.handle_401(resp)
    
    retry_req = mock_connection.send.call_args[0][0]
    auth_header = retry_req.headers["Authorization"]
    
    # According to RFC 2069 / Implementation:
    # If not qop: response = KD(HA1, f"{nonce}:{HA2}")
    # Header should NOT contain qop, nc, cnonce
    
    assert 'realm="legacy"' in auth_header
    assert 'nonce="legacy_nonce"' in auth_header
    assert 'response="' in auth_header
    
    assert "qop=" not in auth_header
    assert "nc=" not in auth_header
    assert "cnonce=" not in auth_header