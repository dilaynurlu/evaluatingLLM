import hashlib
import re
from unittest.mock import Mock
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_sha256_success():
    """
    Test SHA-256 Digest Authentication flow.
    Verifies that the algorithm='SHA-256' parameter is respected and used for hashing.
    Refined with robust parsing.
    """
    username = "user256"
    password = "password256"
    url = "http://example.com/api"
    method = "POST"
    
    auth = HTTPDigestAuth(username, password)
    req = Request(method, url).prepare()
    auth(req) # Initialize state
    
    resp = Response()
    resp.request = req
    resp.status_code = 401
    nonce = "mnonce"
    realm = "realm256"
    
    # SHA-256 in challenge
    challenge = f'Digest realm="{realm}", nonce="{nonce}", qop="auth", algorithm="SHA-256"'
    resp.headers['www-authenticate'] = challenge
    
    resp._content = b""
    resp.raw = Mock()
    resp.raw._original_response = None
    
    mock_connection = Mock()
    sent_resp = Response()
    sent_resp.status_code = 200
    sent_resp.history = []
    mock_connection.send.return_value = sent_resp
    resp.connection = mock_connection
    
    # Execute
    auth.handle_401(resp)
    
    # Verify
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers['Authorization']
    
    # Robust Regex Parsing
    def get_auth_param(name, header):
        pattern = re.compile(f'{name}=(?:"([^"]+)"|([^, ]+))')
        match = pattern.search(header)
        if match:
            return match.group(1) or match.group(2)
        return None

    assert get_auth_param('algorithm', auth_header) == "SHA-256"
    
    # Verify Hash Calculation with SHA-256
    def sha256_utf8(s):
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    ha1 = sha256_utf8(f"{username}:{realm}:{password}")
    ha2 = sha256_utf8(f"{method}:/api")
    
    cnonce = get_auth_param('cnonce', auth_header)
    nc = get_auth_param('nc', auth_header)
    qop = get_auth_param('qop', auth_header)
    
    expected_resp = sha256_utf8(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")
    
    assert get_auth_param('response', auth_header) == expected_resp