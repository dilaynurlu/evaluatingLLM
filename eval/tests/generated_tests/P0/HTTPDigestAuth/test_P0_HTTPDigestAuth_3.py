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
def test_httpdigestauth_handle_401_multiple_challenges_and_algorithms(mock_ctime, mock_urandom, mock_parse_dict_header_func):
    """
    Test handle_401 with multiple challenges, ensuring nonce_count increments
    and different algorithms (SHA-256, MD5-SESS) and qop states are handled.
    Also tests the num_401_calls limit.
    """
    username = "diffuser"
    password = "diffpass"
    auth = HTTPDigestAuth(username, password)

    # Initialize thread-local state
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1

    # --- First Challenge: MD5, qop='auth', establishes last_nonce and nonce_count=1 ---
    mock_original_request_1 = MagicMock(spec=Request)
    mock_original_request_1.url = "http://example.com/api/data"
    mock_original_request_1.method = "POST"
    mock_original_request_1.headers = CaseInsensitiveDict({"Content-Type": "application/json"})
    mock_original_request_1.body = MockBody(initial_pos=20)
    mock_original_request_1._cookies = MagicMock()

    mock_response_1 = MagicMock(spec=Response)
    mock_response_1.status_code = 401
    mock_response_1.request = mock_original_request_1
    mock_response_1.connection = MagicMock()
    mock_response_1.headers = CaseInsensitiveDict({
        "WWW-Authenticate": 'Digest realm="API Realm", nonce="first_nonce_val", qop="auth", algorithm="MD5-SESS"'
    })
    mock_response_1.content = b"Auth Required"
    mock_response_1.close = MagicMock()
    mock_response_1.raw = MagicMock()

    mock_prepared_request_1 = MagicMock(spec=PreparedRequest)
    mock_prepared_request_1.method = mock_original_request_1.method
    mock_prepared_request_1.url = mock_original_request_1.url
    mock_prepared_request_1.headers = CaseInsensitiveDict()
    mock_prepared_request_1._cookies = MagicMock()
    mock_prepared_request_1.prepare_cookies = MagicMock()
    mock_original_request_1.copy.return_value = mock_prepared_request_1

    mock_sent_response_1 = MagicMock(spec=Response)
    mock_sent_response_1.history = []
    mock_response_1.connection.send.return_value = mock_sent_response_1

    # Mock parse_dict_header for the first call
    mock_parse_dict_header_func.side_effect = [
        {
            "realm": "API Realm",
            "nonce": "first_nonce_val",
            "qop": "auth",
            "algorithm": "MD5-SESS"
        }
    ]

    # Perform first challenge
    auth.handle_401(mock_response_1)

    auth_header_1 = mock_prepared_request_1.headers.get("Authorization")
    parsed_header_1 = parse_digest_header(auth_header_1)

    assert parsed_header_1["nc"] == "00000001"
    assert parsed_header_1["algorithm"] == "MD5-SESS"
    assert parsed_header_1["qop"] == "auth"
    assert auth._thread_local.last_nonce == "first_nonce_val"
    assert auth._thread_local.nonce_count == 1
    assert auth._thread_local.num_401_calls == 2 # Max calls after first 401 response

    # --- Second Challenge: Same nonce, different algorithm (SHA-256), no qop ---
    # This should increment nonce_count
    mock_original_request_2 = MagicMock(spec=Request)
    mock_original_request_2.url = "http://example.com/api/data"
    mock_original_request_2.method = "POST"
    mock_original_request_2.headers = CaseInsensitiveDict({"Content-Type": "application/json"})
    mock_original_request_2.body = MockBody(initial_pos=20)
    mock_original_request_2._cookies = MagicMock()

    mock_response_2 = MagicMock(spec=Response)
    mock_response_2.status_code = 401
    mock_response_2.request = mock_original_request_2
    mock_response_2.connection = MagicMock()
    mock_response_2.headers = CaseInsensitiveDict({
        "WWW-Authenticate": 'Digest realm="API Realm", nonce="first_nonce_val", algorithm="SHA-256", opaque="newopaque"'
    })
    mock_response_2.content = b"Auth Required"
    mock_response_2.close = MagicMock()
    mock_response_2.raw = MagicMock()

    mock_prepared_request_2 = MagicMock(spec=PreparedRequest)
    mock_prepared_request_2.method = mock_original_request_2.method
    mock_prepared_request_2.url = mock_original_request_2.url
    mock_prepared_request_2.headers = CaseInsensitiveDict()
    mock_prepared_request_2._cookies = MagicMock()
    mock_prepared_request_2.prepare_cookies = MagicMock()
    mock_original_request_2.copy.return_value = mock_prepared_request_2

    mock_sent_response_2 = MagicMock(spec=Response)
    mock_sent_response_2.history = []
    mock_response_2.connection.send.return_value = mock_sent_response_2

    # Add mock for parse_dict_header for the second call
    mock_parse_dict_header_func.side_effect.append(
        {
            "realm": "API Realm",
            "nonce": "first_nonce_val",
            "algorithm": "SHA-256",
            "opaque": "newopaque"
        }
    )

    # Perform second challenge
    auth.handle_401(mock_response_2)

    auth_header_2 = mock_prepared_request_2.headers.get("Authorization")
    parsed_header_2 = parse_digest_header(auth_header_2)

    assert parsed_header_2["nc"] == "00000002" # Nonce count incremented
    assert parsed_header_2["algorithm"] == "SHA-256"
    assert "qop" not in parsed_header_2 # No qop in challenge
    assert parsed_header_2["opaque"] == "newopaque"
    assert auth._thread_local.last_nonce == "first_nonce_val"
    assert auth._thread_local.nonce_count == 2
    assert auth._thread_local.num_401_calls == 3 # Increased beyond the limit (temporarily)

    # --- Third Call: Same nonce, num_401_calls limit reached ---
    # This should return the original response without re-sending
    mock_original_request_3 = MagicMock(spec=Request)
    mock_original_request_3.url = "http://example.com/api/data"
    mock_original_request_3.method = "POST"
    mock_original_request_3.headers = CaseInsensitiveDict({"Content-Type": "application/json"})
    mock_original_request_3.body = MockBody(initial_pos=20)
    mock_original_request_3._cookies = MagicMock()

    mock_response_3 = MagicMock(spec=Response)
    mock_response_3.status_code = 401
    mock_response_3.request = mock_original_request_3
    mock_response_3.connection = MagicMock()
    mock_response_3.connection.send = MagicMock() # Should not be called
    mock_response_3.headers = CaseInsensitiveDict({
        "WWW-Authenticate": 'Digest realm="API Realm", nonce="first_nonce_val", algorithm="MD5"'
    })
    mock_response_3.content = b"Auth Required"
    mock_response_3.close = MagicMock()
    mock_response_3.raw = MagicMock()

    # The side_effect for mock_parse_dict_header_func is exhausted,
    # it would raise an IndexError if it were called again,
    # which is exactly what we want to ensure: it should NOT be called.

    # num_401_calls is currently 3 (set by previous call)
    result_response_3 = auth.handle_401(mock_response_3)

    # Assert that connection.send was NOT called
    mock_response_3.connection.send.assert_not_called()
    mock_original_request_3.copy.assert_not_called()
    mock_parse_dict_header_func.assert_called_times(2) # Only called for the first two challenges

    # Assert that the original response was returned
    assert result_response_3 is mock_response_3
    # num_401_calls should be reset to 1
    assert auth._thread_local.num_401_calls == 1

    # Verify calculation for SHA-256 (for the second challenge)
    # HA1 = SHA256(username:realm:password)
    A1_sha256 = f"{username}:API Realm:{password}"
    HA1_sha256 = hashlib.sha256(A1_sha256.encode("utf-8")).hexdigest()

    # HA2 = SHA256(method:uri)
    A2_sha256 = f"POST:/api/data"
    HA2_sha256 = hashlib.sha256(A2_sha256.encode("utf-8")).hexdigest()

    # cnonce generation: hashlib.sha1(str(nonce_count).encode + nonce.encode + time.ctime().encode + os.urandom(8)).hexdigest()[:16]
    s_cnonce_2 = str(2).encode("utf-8") + "first_nonce_val".encode("utf-8") + mock_ctime.return_value.encode("utf-8") + mock_urandom.return_value
    expected_cnonce_2 = hashlib.sha1(s_cnonce_2).hexdigest()[:16]
    assert parsed_header_2["cnonce"] == expected_cnonce_2

    # respdig = KD(HA1, nonce:HA2) (since qop is not present)
    expected_respdig_sha256 = hashlib.sha256(f"{HA1_sha256}:first_nonce_val:{HA2_sha256}".encode("utf-8")).hexdigest()
    assert parsed_header_2["response"] == expected_respdig_sha256