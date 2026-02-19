import pytest
import re
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_legacy_no_qop():
    """
    Test legacy Digest Authentication (RFC 2069) where 'qop' is missing.
    Refined to verify correct legacy hash calculation (no nc/cnonce).
    """
    username = "user"
    password = "pass"
    realm = "testrealm"
    nonce = "nonceval"
    uri = "/"
    method = "GET"

    auth = HTTPDigestAuth(username, password)
    req = Request(method, "http://example.com" + uri).prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    # Challenge without qop
    resp.headers = CaseInsensitiveDict({
        "www-authenticate": f'Digest realm="{realm}", nonce="{nonce}"'
    })
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    resp.raw = Mock()
    resp._content = b""
    
    auth.handle_401(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # Assert specific fields are missing
    assert "qop=" not in auth_header
    assert "nc=" not in auth_header
    assert "cnonce=" not in auth_header
    
    def get_val(key):
        match = re.search(f'{key}="?([^",]+)"?', auth_header)
        return match.group(1) if match else None

    # Verify Legacy Hash
    # HA1 = MD5(username:realm:password)
    a1 = f"{username}:{realm}:{password}".encode('utf-8')
    ha1 = hashlib.md5(a1).hexdigest()
    
    # HA2 = MD5(method:uri)
    a2 = f"{method}:{uri}".encode('utf-8')
    ha2 = hashlib.md5(a2).hexdigest()
    
    # Legacy Response = MD5(HA1:nonce:HA2)
    data = f"{ha1}:{nonce}:{ha2}".encode('utf-8')
    expected_response = hashlib.md5(data).hexdigest()
    
    assert get_val("response") == expected_response