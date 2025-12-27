import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth

def test_handle_401_sha256_qop_auth():
    """
    Test Digest Auth with SHA-256 algorithm and qop=auth.
    Should include cnonce, nc, and qop in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    response_401 = Mock()
    response_401.status_code = 401
    response_401.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n", algorithm="SHA-256", qop="auth"'
    }
    response_401.is_redirect = False
    
    original_req = Mock()
    original_req.url = "http://example.com/"
    original_req.method = "GET"
    original_req.headers = {}
    original_req._cookies = Mock()
    
    new_req = Mock()
    new_req.headers = {}
    new_req.method = "GET"
    new_req.url = "http://example.com/"
    original_req.copy.return_value = new_req
    
    response_401.request = original_req
    response_401.connection.send.return_value = Mock(history=[])
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth(original_req)
        auth.handle_401(response_401)
        
    auth_header = new_req.headers["Authorization"]
    assert 'algorithm="SHA-256"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert 'cnonce="' in auth_header