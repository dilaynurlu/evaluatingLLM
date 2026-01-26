import pytest
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_md5_sess():
    """
    Test Digest Authentication with algorithm=MD5-sess.
    HA1 should be MD5(MD5(username:realm:password):nonce:cnonce).
    """
    username = "user"
    password = "password"
    realm = "sess-realm"
    nonce = "sess-nonce"
    method = "GET"
    path = "/"
    url = f"http://example.com{path}"
    
    auth = HTTPDigestAuth(username, password)
    request = Request(method, url).prepare()
    auth(request)

    response_401 = Response()
    response_401.status_code = 401
    response_401.request = request
    response_401.url = url
    response_401.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", algorithm="MD5-sess", qop="auth"'
    response_401._content = b""
    response_401.raw = Mock()

    mock_connection = Mock()
    response_401.connection = mock_connection
    mock_connection.send.return_value = Response()

    auth.handle_401(response_401)
    
    retry_request = mock_connection.send.call_args[0][0]
    auth_header = retry_request.headers["Authorization"]
    
    parts = {}
    for part in auth_header[7:].split(", "):
        key, val = part.split("=", 1)
        val = val.strip('"')
        parts[key] = val
        
    cnonce = parts["cnonce"]
    nc = parts["nc"]
    qop = parts["qop"]
    
    # Verify MD5-sess specific HA1 calculation
    step1 = hashlib.md5(f"{username}:{realm}:{password}".encode("utf-8")).hexdigest()
    ha1_sess = hashlib.md5(f"{step1}:{nonce}:{cnonce}".encode("utf-8")).hexdigest()
    ha2 = hashlib.md5(f"{method}:{path}".encode("utf-8")).hexdigest()
    
    expected_resp = hashlib.md5(f"{ha1_sess}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode("utf-8")).hexdigest()
    
    assert parts["algorithm"] == "MD5-SESS"
    assert parts["response"] == expected_resp