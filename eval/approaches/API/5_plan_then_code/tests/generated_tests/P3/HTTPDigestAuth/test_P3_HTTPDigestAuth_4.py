import hashlib
import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_md5_sess():
    """
    Test MD5-SESS Algorithm.
    Verifies HA1 construction: MD5(MD5(username:realm:password):nonce:cnonce).
    """
    username = "user"
    password = "pass"
    realm = "sess_realm"
    nonce = "sess_nonce"
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
    response.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", algorithm="MD5-SESS", qop="auth"'
    
    response.connection = Mock()
    response.connection.send.return_value = Response()
    
    fixed_salt = b"salt"
    fixed_time = "time"
    
    with patch("os.urandom", return_value=fixed_salt), \
         patch("time.ctime", return_value=fixed_time):
        auth.handle_401(response)
        
    sent_req = response.connection.send.call_args[0][0]
    header = sent_req.headers["Authorization"]
    parts = header[7:].split(", ")
    header_dict = {k: v.strip('"') for k, v in [p.split("=", 1) for p in parts]}
    
    assert header_dict['algorithm'] == 'MD5-SESS'
    
    # Independent verification
    def md5(x): return hashlib.md5(x.encode("utf-8")).hexdigest()
    
    # cnonce
    s = b"1" + nonce.encode("utf-8") + fixed_time.encode("utf-8") + fixed_salt
    expected_cnonce = hashlib.sha1(s).hexdigest()[:16]
    
    # MD5-SESS HA1 logic
    step1 = md5(f"{username}:{realm}:{password}")
    ha1 = md5(f"{step1}:{nonce}:{expected_cnonce}")
    ha2 = md5(f"{method}:{uri}")
    expected_resp = md5(f"{ha1}:{nonce}:00000001:{expected_cnonce}:auth:{ha2}")
    
    assert header_dict['cnonce'] == expected_cnonce
    assert header_dict['response'] == expected_resp