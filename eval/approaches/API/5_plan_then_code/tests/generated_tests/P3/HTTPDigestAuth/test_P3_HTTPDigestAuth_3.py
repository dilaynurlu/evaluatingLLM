import hashlib
import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_no_qop_legacy():
    """
    Test Legacy Digest Authentication (RFC 2069).
    Verifies that when 'qop' is missing:
    1. 'cnonce' and 'nc' are NOT present in the Authorization header.
    2. The hash construction uses the RFC 2069 format: MD5(HA1:nonce:HA2).
    """
    username = "user"
    password = "pass"
    realm = "Legacy"
    nonce = "legacynonce"
    method = "GET"
    uri = "/"
    
    auth = HTTPDigestAuth(username, password)
    req = Request(method, "http://example.com/").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.request = req
    response.url = "http://example.com/"
    response._content = b""
    # No qop
    response.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}"'
    
    response.connection = Mock()
    response.connection.send.return_value = Response()
    
    auth.handle_401(response)
    
    sent_req = response.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    # Parse header
    parts = auth_header[7:].split(", ")
    header_dict = {k: v.strip('"') for k, v in [p.split("=", 1) for p in parts]}
    
    # Assertions
    assert "qop" not in header_dict
    assert "cnonce" not in header_dict
    assert "nc" not in header_dict
    
    # RFC 2069 Calculation
    def md5(x): return hashlib.md5(x.encode("utf-8")).hexdigest()
    ha1 = md5(f"{username}:{realm}:{password}")
    ha2 = md5(f"{method}:{uri}")
    expected_resp = md5(f"{ha1}:{nonce}:{ha2}")
    
    assert header_dict['response'] == expected_resp