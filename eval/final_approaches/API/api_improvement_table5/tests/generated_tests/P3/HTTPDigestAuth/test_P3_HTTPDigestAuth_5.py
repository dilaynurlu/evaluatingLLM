import pytest
import re
import hashlib
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_sha512_algorithm():
    """
    Test Digest Authentication using the SHA-512 algorithm.
    Refined to verify the exact SHA-512 hash calculation.
    """
    username = "user"
    password = "pass"
    realm = "realm"
    nonce = "nonce"
    uri = "/"
    method = "GET"
    algo = "SHA-512"
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

    cnonce = get_val("cnonce")
    nc = get_val("nc")
    
    # Verify Hash
    a1 = f"{username}:{realm}:{password}".encode('utf-8')
    ha1 = hashlib.sha512(a1).hexdigest()
    
    a2 = f"{method}:{uri}".encode('utf-8')
    ha2 = hashlib.sha512(a2).hexdigest()
    
    data = f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode('utf-8')
    expected_response = hashlib.sha512(data).hexdigest()
    
    actual_response = get_val("response")
    
    assert len(actual_response) == 128
    assert actual_response == expected_response
    assert get_val("algorithm") == algo