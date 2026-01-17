import pytest
from unittest.mock import Mock, patch
import requests
from requests.auth import HTTPDigestAuth
import hashlib

def test_http_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication with SHA-256 algorithm.
    Verifies that the generated header uses SHA-256 for the hash calculation.
    """
    url = "http://example.org/secure"
    username = "user"
    password = "pass"
    realm = "realm"
    nonce = "n"
    algorithm = "SHA-256"
    
    auth = HTTPDigestAuth(username, password)
    
    req = requests.Request("GET", url).prepare()
    
    resp_401 = requests.Response()
    resp_401.request = req
    resp_401.url = url
    resp_401.status_code = 401
    resp_401.headers["www-authenticate"] = (
        f'Digest realm="{realm}", nonce="{nonce}", qop="auth", algorithm="{algorithm}"'
    )
    resp_401._content = b""
    resp_401.raw = Mock()
    
    mock_connection = Mock()
    resp_success = requests.Response()
    resp_success.status_code = 200
    mock_connection.send = Mock(return_value=resp_success)
    resp_401.connection = mock_connection
    
    # Fix cnonce for deterministic calc
    fixed_cnonce_hex = "aabbccddeeff0011"
    fixed_cnonce_bytes = bytes.fromhex(fixed_cnonce_hex)
    
    with patch("os.urandom", return_value=fixed_cnonce_bytes):
        auth(req)
        auth.handle_401(resp_401)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    assert f'algorithm="{algorithm}"' in auth_header
    
    # Validation of SHA-256 Calculation
    # HA1 = SHA256(username:realm:password)
    a1 = f"{username}:{realm}:{password}"
    ha1 = hashlib.sha256(a1.encode("utf-8")).hexdigest()
    
    # HA2 = SHA256(method:uri)
    a2 = f"GET:/secure"
    ha2 = hashlib.sha256(a2.encode("utf-8")).hexdigest()
    
    # Response = SHA256(HA1:nonce:nc:cnonce:qop:HA2)
    resp_input = f"{ha1}:{nonce}:00000001:{fixed_cnonce_hex}:auth:{ha2}"
    expected_response = hashlib.sha256(resp_input.encode("utf-8")).hexdigest()
    
    assert f'response="{expected_response}"' in auth_header