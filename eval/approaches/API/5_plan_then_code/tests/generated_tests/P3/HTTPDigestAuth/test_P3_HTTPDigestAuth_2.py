import hashlib
import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_sha256_utf8_kat():
    """
    Test SHA-256 Digest Authentication with UTF-8 characters.
    Verifies proper handling of unicode in username/realm using a Reference Implementation check.
    """
    # Inputs with Unicode
    username = "München"
    password = "p@ssword€"
    realm = "WallyWorld"
    nonce = "randomnonce"
    method = "GET"
    uri = "/api/utf8"
    
    auth = HTTPDigestAuth(username, password)
    req = Request(method, f"http://example.com{uri}").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.request = req
    response.url = f"http://example.com{uri}"
    response._content = b""
    # Challenge
    response.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", qop="auth", algorithm="SHA-256"'
    
    response.connection = Mock()
    response.connection.send.return_value = Response()
    
    # Control randomness
    fixed_salt = b"salt"
    fixed_time = "time"
    
    with patch("os.urandom", return_value=fixed_salt), \
         patch("time.ctime", return_value=fixed_time):
        auth.handle_401(response)
        
    sent_req = response.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    # Reference Implementation for Verification
    # Digest Auth implies hashing UTF-8 bytes if not specified otherwise in requests
    def sha256(data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    def sha1(data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha1(data).hexdigest()

    # Replicate requests cnonce logic strictly
    s = b"1" + nonce.encode('utf-8') + fixed_time.encode('utf-8') + fixed_salt
    expected_cnonce = sha1(s)[:16]
    
    ha1 = sha256(f"{username}:{realm}:{password}")
    ha2 = sha256(f"{method}:{uri}")
    nc = "00000001"
    qop = "auth"
    expected_resp_val = sha256(f"{ha1}:{nonce}:{nc}:{expected_cnonce}:{qop}:{ha2}")
    
    # Parse header
    parts = auth_header[7:].split(", ")
    header_dict = {k: v.strip('"') for k, v in [p.split("=", 1) for p in parts]}
    
    assert header_dict['algorithm'] == 'SHA-256'
    assert header_dict['username'] == username # Should be preserved or encoded? Requests usually sends raw string in header if possible or latin1.
    assert header_dict['cnonce'] == expected_cnonce
    assert header_dict['response'] == expected_resp_val