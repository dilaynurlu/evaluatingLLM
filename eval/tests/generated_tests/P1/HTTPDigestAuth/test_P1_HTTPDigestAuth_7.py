import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_md5_sess_algorithm():
    """
    Test Digest Auth with MD5-SESS algorithm.
    It has specific logic for HA1 calculation involving nonce and cnonce.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = MagicMock(spec=requests.PreparedRequest)
    req.method = "GET"
    req.url = "http://example.com"
    req.body = None
    req.register_hook = MagicMock()
    auth(req)
    
    # Prepare state manually to test build_digest_header specifically
    # or use handle_401 flow. Using handle_401 for integration coverage.
    
    r_401 = MagicMock(spec=requests.Response)
    r_401.request = req
    
    new_req = MagicMock(spec=requests.PreparedRequest)
    new_req.headers = {}
    new_req.method = "GET"
    new_req.url = "http://example.com"
    new_req._cookies = MagicMock()
    new_req.prepare_cookies = MagicMock()
    req.copy.return_value = new_req
    
    r_401.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n", algorithm="MD5-SESS", qop="auth"'
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
    assert 'algorithm="MD5-SESS"' in auth_header
    assert 'nonce="n"' in auth_header
    # HA1 for MD5-SESS involves cnonce, so verification implies correct flow execution.