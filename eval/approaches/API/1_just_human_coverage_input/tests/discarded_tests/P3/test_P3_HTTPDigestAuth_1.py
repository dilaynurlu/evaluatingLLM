import pytest
from unittest.mock import Mock, patch
import requests
from requests.auth import HTTPDigestAuth
import hashlib

def test_http_digest_auth_md5_flow():
    """
    Test the standard Digest Authentication flow using MD5, qop="auth", and opaque data.
    Verifies that the Authorization header contains the mathematically correct response
    and echoes the opaque value.
    """
    url = "http://example.org/resource"
    username = "user"
    password = "pass"
    realm = "testrealm"
    nonce = "nonce123"
    opaque = "opaque-data-value"
    cnonce = "cnonce123"
    
    auth = HTTPDigestAuth(username, password)
    
    # 1. Prepare a Request
    req = requests.Request("GET", url).prepare()
    
    # 2. Setup the initial 401 Response
    resp_401 = requests.Response()
    resp_401.request = req
    resp_401.url = url
    resp_401.status_code = 401
    resp_401.reason = "Unauthorized"
    # Challenge includes opaque to ensure it is echoed back
    resp_401.headers["www-authenticate"] = (
        f'Digest realm="{realm}", nonce="{nonce}", qop="auth", opaque="{opaque}"'
    )
    resp_401._content = b""
    
    mock_raw = Mock()
    resp_401.raw = mock_raw
    
    mock_connection = Mock()
    resp_success = requests.Response()
    resp_success.status_code = 200
    resp_success.request = req 
    resp_success.connection = mock_connection
    resp_success._content = b"Success"
    
    mock_connection.send = Mock(return_value=resp_success)
    resp_401.connection = mock_connection

    # 3. Patch os.urandom to generate a deterministic cnonce
    # The implementation often uses os.urandom(8) -> hex. 
    # We mock it to return a known byte sequence that produces a known hex string if possible,
    # or patch the method generating the cnonce if strictly necessary. 
    # However, requests.auth uses os.urandom(8).
    # Let's patch os.urandom to return bytes that are traceable, but requests converts to hex.
    # Easier strategy: Patch the _thread_local context or the cnonce generation logic?
    # No, let's patch os.urandom.
    
    # Logic in requests: cnonce = (os.urandom(8)).encode('hex') (Py2) or binascii.hexlify (Py3)
    # We want cnonce="cnonce123". This is 16 hex chars (8 bytes).
    # "cnonce123" is 9 chars, invalid for 8 bytes hex. 
    # Let's use a valid hex string for cnonce: "0102030405060708"
    fixed_cnonce_hex = "0102030405060708"
    fixed_cnonce_bytes = bytes.fromhex(fixed_cnonce_hex)
    
    with patch("os.urandom", return_value=fixed_cnonce_bytes):
        # Initialize auth hooks
        auth(req)
        # Trigger the 401 handling
        final_response = auth.handle_401(resp_401)
    
    # 4. Assertions
    assert final_response.status_code == 200
    assert mock_connection.send.call_count == 1
    
    args, _ = mock_connection.send.call_args
    sent_request = args[0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert auth_header is not None
    assert 'Digest ' in auth_header
    assert f'username="{username}"' in auth_header
    assert f'realm="{realm}"' in auth_header
    assert f'nonce="{nonce}"' in auth_header
    assert 'uri="/resource"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert f'cnonce="{fixed_cnonce_hex}"' in auth_header
    assert f'opaque="{opaque}"' in auth_header
    
    # 5. Verify Cryptographic Correctness
    # HA1 = MD5(username:realm:password)
    a1 = f"{username}:{realm}:{password}"
    ha1 = hashlib.md5(a1.encode("utf-8")).hexdigest()
    
    # HA2 = MD5(method:uri)
    a2 = f"GET:/resource"
    ha2 = hashlib.md5(a2.encode("utf-8")).hexdigest()
    
    # Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
    resp_input = f"{ha1}:{nonce}:00000001:{fixed_cnonce_hex}:auth:{ha2}"
    expected_response = hashlib.md5(resp_input.encode("utf-8")).hexdigest()
    
    assert f'response="{expected_response}"' in auth_header