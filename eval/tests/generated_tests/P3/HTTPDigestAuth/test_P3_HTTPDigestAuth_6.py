import hashlib
import re
from unittest.mock import Mock
import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_md5_sess_algorithm():
    """
    Test MD5-SESS algorithm support.
    For MD5-SESS, HA1 is calculated differently:
    HA1 = MD5(MD5(username:realm:password):nonce:cnonce)
    Refined with robust parsing.
    """
    username = "sess_user"
    password = "sess_password"
    realm = "sess_realm"
    nonce = "sess_nonce"
    
    auth = HTTPDigestAuth(username, password)
    req = Request('GET', 'http://sess.com/').prepare()
    auth(req)
    
    resp = Response()
    resp.request = req
    resp.status_code = 401
    challenge = f'Digest realm="{realm}", nonce="{nonce}", qop="auth", algorithm="MD5-SESS"'
    resp.headers['www-authenticate'] = challenge
    
    resp._content = b""
    resp.raw = Mock()
    resp.raw._original_response = None
    
    mock_conn = Mock()
    mock_conn.send.return_value = Response()
    mock_conn.send.return_value.history = []
    resp.connection = mock_conn
    
    auth.handle_401(resp)
    
    auth_header = mock_conn.send.call_args[0][0].headers['Authorization']
    
    # Robust Regex Parsing
    def get_auth_param(name, header):
        pattern = re.compile(f'{name}=(?:"([^"]+)"|([^, ]+))')
        match = pattern.search(header)
        if match:
            return match.group(1) or match.group(2)
        return None
            
    assert get_auth_param('algorithm', auth_header) == 'MD5-SESS'
    
    cnonce = get_auth_param('cnonce', auth_header)
    nc = get_auth_param('nc', auth_header)
    qop = get_auth_param('qop', auth_header)
    
    # HA1 calculation for MD5-SESS
    # HA1 = MD5( MD5(username:realm:password) : nonce : cnonce )
    def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
    
    step1 = md5(f"{username}:{realm}:{password}")
    ha1 = md5(f"{step1}:{nonce}:{cnonce}")
    
    ha2 = md5(f"GET:/")
    
    expected_resp = md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")
    
    assert get_auth_param('response', auth_header) == expected_resp