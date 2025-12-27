import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_no_qop_fallback():
    """
    Test Digest Auth behavior when 'qop' is missing in the challenge.
    Should fallback to RFC 2069 (no cnonce, no nc).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = MagicMock(spec=requests.PreparedRequest)
    req.method = "GET"
    req.url = "http://example.com"
    req.body = None
    req.register_hook = MagicMock()
    auth(req)
    
    r_401 = MagicMock(spec=requests.Response)
    r_401.request = req
    
    new_req = MagicMock(spec=requests.PreparedRequest)
    new_req.headers = {}
    new_req.method = "GET"
    new_req.url = "http://example.com"
    new_req._cookies = MagicMock()
    new_req.prepare_cookies = MagicMock()
    req.copy.return_value = new_req
    
    # Challenge without qop
    r_401.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n"'
    }
    r_401.status_code = 401
    r_401.is_redirect = False
    r_401.content = b""
    r_401.raw = MagicMock()
    r_401.connection = MagicMock()
    r_401.connection.send.return_value = MagicMock()
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth.handle_401(r_401)
        
    auth_header = new_req.headers.get("Authorization")
    assert auth_header.startswith("Digest ")
    
    # Should NOT contain qop, cnonce, or nc
    assert "qop=" not in auth_header
    assert "cnonce=" not in auth_header
    assert "nc=" not in auth_header
    assert 'response="' in auth_header