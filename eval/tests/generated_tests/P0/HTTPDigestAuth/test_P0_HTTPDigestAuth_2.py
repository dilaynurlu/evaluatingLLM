import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
import hashlib
import os
import time
from urllib.parse import urlparse

# Helper for parsing digest header to assert values easily
def parse_digest_header(header_value):
    if not header_value.startswith("Digest "):
        return {}
    parts = header_value[len("Digest "):].split(', ')
    parsed_dict = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            parsed_dict[key.strip()] = value.strip().strip('"')
    return parsed_dict

# Mock for `r.body.tell()` and `r.body.seek()`
class MockBody:
    def __init__(self, initial_pos=0):
        self._pos = initial_pos
        self.size = 100 # Example size

    def tell(self):
        return self._pos

    def seek(self, pos):
        self._pos = pos

    # For `r.content` in `handle_401`
    def read(self, size=None):
        return b"mock content"

    def __iter__(self):
        yield b"mock content"


@patch('requests.utils.parse_dict_header')
@patch('os.urandom', return_value=b'cnonce_entropy')
@patch('time.ctime', return_value='Mon Jan 1 00:00:00 2000')
def test_httpdigestauth_handle_401_md5_auth_qop(mock_ctime, mock_urandom, mock_parse_dict_header_func):
    """
    Test handle_401 behavior with a standard MD5 Digest challenge and qop='auth'.
    Verifies that a new request is sent with the correct Authorization header.
    """
    username = "testuser"
    password = "testpass"
    auth = HTTPDigestAuth(username, password)

    # Initialize thread-local state (as if __call__ was already invoked)
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1 # Simulate initial call before 401 response

    # Mock the original request that received the 401
    mock_original_request = MagicMock(spec=Request)
    mock_original_request.url = "http://example.com/secure_path?key=value"
    mock_original_request.method = "GET"
    mock_original_request.headers = CaseInsensitiveDict()
    mock_original_request.body = MockBody(initial_pos=10) # Simulate body position
    mock_original_request._cookies = MagicMock()

    # Mock the 401 Response object
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 401
    mock_response.is_redirect = False
    mock_response.request = mock_original_request
    mock_response.connection = MagicMock()
    mock_response.connection.send = MagicMock() # This is where the new request is sent
    mock_response.headers = CaseInsensitiveDict({
        "WWW-Authenticate": 'Digest realm="Test Realm", nonce="somenonce123", qop="auth", algorithm="MD5", opaque="someopaque"'
    })
    mock_response.content = b"Auth Required" # Accessed in handle_401
    mock_response.close = MagicMock()
    mock_response.raw = MagicMock() # For extract_cookies_to_jar

    # Mock the behavior of requests.utils.parse_dict_header
    expected_chal = {
        "realm": "Test Realm",
        "nonce": "somenonce123",
        "qop": "auth",
        "algorithm": "MD5",
        "opaque": "someopaque"
    }
    mock_parse_dict_header_func.return_value = expected_chal

    # Mock the PreparedRequest that `r.request.copy()` would return
    mock_prepared_request = MagicMock(spec=PreparedRequest)
    mock_prepared_request.method = mock_original_request.method
    mock_prepared_request.url = mock_original_request.url
    mock_prepared_request.headers = CaseInsensitiveDict()
    mock_prepared_request._cookies = MagicMock() # For prepare_cookies
    mock_prepared_request.prepare_cookies = MagicMock()

    mock_original_request.copy.return_value = mock_prepared_request

    # Mock the response from sending the new prepared request
    mock_sent_response = MagicMock(spec=Response)
    mock_sent_response.history = [] # Simulate an empty history
    mock_response.connection.send.return_value = mock_sent_response

    # Call handle_401
    result_response = auth.handle_401(mock_response)

    # Assertions
    mock_original_request.body.seek.assert_called_once_with(auth._thread_local.pos)
    mock_parse_dict_header_func.assert_called_once_with(
        'realm="Test Realm", nonce="somenonce123", qop="auth", algorithm="MD5", opaque="someopaque"'
    )
    mock_original_request.copy.assert_called_once()
    mock_prepared_request.prepare_cookies.assert_called_once()

    # Verify connection.send was called with the prepared request
    mock_response.connection.send.assert_called_once_with(mock_prepared_request, **{})

    # Verify the returned response
    assert result_response is mock_sent_response
    assert mock_sent_response.history == [mock_response]
    assert mock_sent_response.request is mock_prepared_request

    # Verify the Authorization header
    auth_header = mock_prepared_request.headers.get("Authorization")
    assert auth_header is not None

    parsed_header = parse_digest_header(auth_header)

    assert parsed_header["username"] == username
    assert parsed_header["realm"] == expected_chal["realm"]
    assert parsed_header["nonce"] == expected_chal["nonce"]
    assert parsed_header["uri"] == "/secure_path?key=value"
    assert parsed_header["qop"] == "auth"
    assert parsed_header["nc"] == "00000001" # First call, nonce_count is 1
    assert parsed_header["algorithm"] == "MD5"
    assert parsed_header["opaque"] == expected_chal["opaque"]

    # Calculate expected response digest manually to verify
    # HA1 = MD5(username:realm:password)
    A1 = f"{username}:{expected_chal['realm']}:{password}"
    HA1 = hashlib.md5(A1.encode("utf-8")).hexdigest()

    # HA2 = MD5(method:uri)
    A2 = f"GET:/secure_path?key=value"
    HA2 = hashlib.md5(A2.encode("utf-8")).hexdigest()

    # cnonce generation: hashlib.sha1(str(nonce_count).encode + nonce.encode + time.ctime().encode + os.urandom(8)).hexdigest()[:16]
    s_cnonce = str(1).encode("utf-8") + expected_chal["nonce"].encode("utf-8") + mock_ctime.return_value.encode("utf-8") + mock_urandom.return_value
    expected_cnonce = hashlib.sha1(s_cnonce).hexdigest()[:16]
    assert parsed_header["cnonce"] == expected_cnonce

    # respdig = KD(HA1, nonce:ncvalue:cnonce:qop:HA2)
    noncebit = f"{expected_chal['nonce']}:{parsed_header['nc']}:{expected_cnonce}:auth:{HA2}"
    expected_respdig = hashlib.md5(f"{HA1}:{noncebit}".encode("utf-8")).hexdigest()
    assert parsed_header["response"] == expected_respdig

    assert auth._thread_local.last_nonce == expected_chal["nonce"]
    assert auth._thread_local.nonce_count == 1
    assert auth._thread_local.num_401_calls == 2 # Incremented after sending new request