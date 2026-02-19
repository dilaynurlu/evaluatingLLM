import pytest
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication with SHA-256 algorithm.
    """
    username = "user"
    password = "password"
    realm = "sha256-realm"
    nonce = "somenonce"
    method = "GET"
    path = "/"
    url = f"http://example.com{path}"
    
    # Expected calculations with SHA-256
    def sha256_utf8(s):
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    ha1 = sha256_utf8(f"{username}:{realm}:{password}")
    ha2 = sha256_utf8(f"{method}:{path}")
    
    auth = HTTPDigestAuth(username, password)
    request = Request(method, url).prepare()
    auth(request)

    response_401 = Response()
    response_401.status_code = 401
    response_401.request = request
    response_401.url = url
    response_401.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}", algorithm="SHA-256", qop="auth"'
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
        
    assert parts["algorithm"] == "SHA-256"
    
    # Verify hash correctness
    cnonce = parts["cnonce"]
    nc = parts["nc"]
    qop = parts["qop"]
    
    expected_resp = sha256_utf8(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")
    assert parts["response"] == expected_resp