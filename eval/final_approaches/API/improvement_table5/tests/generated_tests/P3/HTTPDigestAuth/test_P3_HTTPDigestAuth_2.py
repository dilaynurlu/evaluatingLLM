import pytest
import re
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication using the SHA-256 algorithm.
    Refined to verify the exact SHA-256 hash calculation.
    """
    username = "user"
    password = "pass"
    realm = "testrealm"
    nonce = "nonceval"
    uri = "/"
    method = "GET"
    algo = "SHA-256"
    qop = "auth"

    auth = HTTPDigestAuth(username, password)
    req = Request(method, "http://example.com" + uri).prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers = CaseInsensitiveDict({
        "www-authenticate": f'Digest realm="{realm}", nonce="{nonce}", algorithm="{algo}", qop="{qop}"'
    })
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    resp.raw = Mock()
    resp._content = b""
    
    auth.handle_401(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    def get_val(key):
        match = re.search(f'{key}="?([^",]+)"?', auth_header)
        return match.group(1) if match else None

    assert get_val("algorithm") == algo
    cnonce = get_val("cnonce")
    nc = get_val("nc")
    
    # Verify Hash
    # HA1 = SHA-256(username:realm:password)
    a1 = f"{username}:{realm}:{password}".encode('utf-8')
    ha1 = hashlib.sha256(a1).hexdigest()
    
    # HA2 = SHA-256(method:uri)
    a2 = f"{method}:{uri}".encode('utf-8')
    ha2 = hashlib.sha256(a2).hexdigest()
    
    # Response = SHA-256(HA1:nonce:nc:cnonce:qop:HA2)
    data = f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode('utf-8')
    expected_response = hashlib.sha256(data).hexdigest()
    
    actual_response = get_val("response")
    assert len(actual_response) == 64
    assert actual_response == expected_response