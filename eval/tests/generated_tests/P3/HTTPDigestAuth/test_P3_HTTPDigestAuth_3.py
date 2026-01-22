import hashlib
import re
from unittest.mock import Mock
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_no_qop_compatibility():
    """
    Test Digest Authentication without 'qop' (RFC 2069 compatibility).
    When qop is missing, the response calculation is simplified:
    Response = KD(HA1, nonce:HA2)
    And headers like 'cnonce' and 'nc' should NOT be present.
    Refined with robust parsing.
    """
    username = "legacy"
    password = "pwd"
    auth = HTTPDigestAuth(username, password)
    req = Request('GET', 'http://old-server.com/data').prepare()
    auth(req)
    
    resp = Response()
    resp.request = req
    resp.status_code = 401
    nonce = "legacynonce"
    realm = "legacyrealm"
    
    # Challenge WITHOUT qop
    challenge = f'Digest realm="{realm}", nonce="{nonce}"'
    resp.headers['www-authenticate'] = challenge
    
    resp._content = b""
    resp.raw = Mock()
    resp.raw._original_response = None
    
    mock_connection = Mock()
    sent_resp = Response()
    sent_resp.history = []
    mock_connection.send.return_value = sent_resp
    resp.connection = mock_connection
    
    auth.handle_401(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers['Authorization']
    
    # Robust Regex Parsing
    def get_auth_param(name, header):
        pattern = re.compile(f'{name}=(?:"([^"]+)"|([^, ]+))')
        match = pattern.search(header)
        if match:
            return match.group(1) or match.group(2)
        return None
            
    # Verify qop, cnonce, nc are missing
    assert get_auth_param('qop', auth_header) is None
    assert get_auth_param('cnonce', auth_header) is None
    assert get_auth_param('nc', auth_header) is None
    
    # Verify Response calculation (Old RFC 2069)
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode('utf-8')).hexdigest()
    ha2 = hashlib.md5(f"GET:/data".encode('utf-8')).hexdigest()
    
    # Response = MD5(HA1:nonce:HA2)
    expected_resp = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode('utf-8')).hexdigest()
    
    assert get_auth_param('response', auth_header) == expected_resp