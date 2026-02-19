import pytest
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_no_qop_legacy():
    """
    Test Digest Authentication without 'qop' (RFC 2069 compatibility).
    Should not include cnonce or nc in hash calculation or header.
    """
    username = "user"
    password = "password"
    realm = "legacy-realm"
    nonce = "legacy-nonce"
    method = "GET"
    path = "/"
    url = f"http://example.com{path}"

    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode("utf-8")).hexdigest()
    ha2 = hashlib.md5(f"{method}:{path}".encode("utf-8")).hexdigest()
    
    # Without qop, Response = MD5(HA1:nonce:HA2)
    expected_response = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode("utf-8")).hexdigest()

    auth = HTTPDigestAuth(username, password)
    request = Request(method, url).prepare()
    auth(request)

    response_401 = Response()
    response_401.status_code = 401
    response_401.request = request
    response_401.url = url
    # No qop in challenge
    response_401.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}"'
    response_401._content = b""
    response_401.raw = Mock()

    mock_connection = Mock()
    response_401.connection = mock_connection
    mock_connection.send.return_value = Response()

    auth.handle_401(response_401)
    
    retry_request = mock_connection.send.call_args[0][0]
    auth_header = retry_request.headers["Authorization"]
    
    assert "qop" not in auth_header
    assert "cnonce" not in auth_header
    assert "nc=" not in auth_header
    
    parts = {k: v.strip('"') for k, v in [p.split("=", 1) for p in auth_header[7:].split(", ")]}
    assert parts["response"] == expected_response