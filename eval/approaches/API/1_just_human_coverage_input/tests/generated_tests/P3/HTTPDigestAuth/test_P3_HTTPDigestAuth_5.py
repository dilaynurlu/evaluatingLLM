import pytest
from unittest.mock import Mock, patch
import requests
from requests.auth import HTTPDigestAuth
import hashlib

def test_http_digest_auth_no_qop():
    """
    Test Digest Authentication when the server does not provide 'qop'.
    This is a backward compatibility mode (RFC 2069).
    Verifies the legacy hash construction (no cnonce/nc).
    """
    url = "http://example.org/legacy"
    username = "user"
    password = "pass"
    realm = "test"
    nonce = "abc"
    
    auth = HTTPDigestAuth(username, password)
    
    req = requests.Request("GET", url).prepare()
    
    resp_401 = requests.Response()
    resp_401.request = req
    resp_401.url = url
    resp_401.status_code = 401
    # Missing qop parameter
    resp_401.headers["www-authenticate"] = f'Digest realm="{realm}", nonce="{nonce}"'
    resp_401._content = b""
    resp_401.raw = Mock()
    
    mock_connection = Mock()
    resp_success = requests.Response()
    resp_success.status_code = 200
    mock_connection.send = Mock(return_value=resp_success)
    resp_401.connection = mock_connection
    
    auth(req)
    auth.handle_401(resp_401)
    
    assert mock_connection.send.call_count == 1
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # In legacy mode (no qop):
    # 'qop', 'nc', and 'cnonce' should NOT be present.
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header
    assert f'nonce="{nonce}"' in auth_header
    
    # Verify Hash for Legacy Mode
    # Response = MD5(HA1:nonce:HA2)
    a1 = f"{username}:{realm}:{password}"
    ha1 = hashlib.md5(a1.encode("utf-8")).hexdigest()
    
    a2 = f"GET:/legacy"
    ha2 = hashlib.md5(a2.encode("utf-8")).hexdigest()
    
    resp_input = f"{ha1}:{nonce}:{ha2}"
    expected_response = hashlib.md5(resp_input.encode("utf-8")).hexdigest()
    
    assert f'response="{expected_response}"' in auth_header