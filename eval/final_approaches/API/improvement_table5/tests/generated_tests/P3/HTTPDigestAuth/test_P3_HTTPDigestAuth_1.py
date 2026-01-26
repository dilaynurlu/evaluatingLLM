import pytest
import re
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_md5_basic():
    """
    Test basic MD5 Digest Authentication flow with qop='auth'.
    Refined to cryptographically verify the response hash and verify robust header parsing.
    """
    username = "user"
    password = "pass"
    realm = "testrealm"
    nonce = "dcd98b7102dd2f0e8b11d0f600bfb0c093"
    uri = "/path"
    method = "GET"
    qop = "auth"
    opaque = "5ccc069c403ebaf9f0171e9517f40e41"

    auth = HTTPDigestAuth(username, password)
    req = Request(method, "http://example.com" + uri).prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers = CaseInsensitiveDict({
        "www-authenticate": f'Digest realm="{realm}", nonce="{nonce}", qop="{qop}", opaque="{opaque}"'
    })
    
    mock_connection = Mock()
    resp.connection = mock_connection
    retry_resp = Response()
    retry_resp.status_code = 200
    mock_connection.send.return_value = retry_resp
    
    resp.raw = Mock()
    resp._content = b""
    
    result = auth.handle_401(resp)
    
    assert mock_connection.send.called
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert auth_header.startswith("Digest ")
    
    # Robust parsing using regex
    def get_val(key):
        match = re.search(f'{key}="?([^",]+)"?', auth_header)
        return match.group(1) if match else None

    assert get_val("username") == username
    assert get_val("realm") == realm
    assert get_val("nonce") == nonce
    assert get_val("uri") == uri
    assert get_val("qop") == qop
    assert get_val("opaque") == opaque
    assert get_val("nc") == "00000001"
    
    cnonce = get_val("cnonce")
    assert cnonce is not None
    
    # Cryptographic Verification
    # HA1 = MD5(username:realm:password)
    a1 = f"{username}:{realm}:{password}".encode('utf-8')
    ha1 = hashlib.md5(a1).hexdigest()
    
    # HA2 = MD5(method:digestURI)
    a2 = f"{method}:{uri}".encode('utf-8')
    ha2 = hashlib.md5(a2).hexdigest()
    
    # Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    response_data = f"{ha1}:{nonce}:00000001:{cnonce}:{qop}:{ha2}".encode('utf-8')
    expected_response = hashlib.md5(response_data).hexdigest()
    
    assert get_val("response") == expected_response
    assert result == retry_resp