import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict
import hashlib
import os
import time
from urllib.parse import urlparse # Used internally by HTTPDigestAuth

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


def test_httpdigestauth_initial_call_and_redirect_handling():
    """
    Test initial __call__ behavior when no previous digest state exists,
    ensuring no Authorization header is set initially and hooks are registered.
    Also tests handle_redirect functionality.
    """
    username = "testuser"
    password = "testpass"
    auth = HTTPDigestAuth(username, password)

    # 1. Test initial __call__
    mock_request = MagicMock(spec=Request)
    mock_request.url = "http://example.com/protected"
    mock_request.method = "GET"
    mock_request.headers = CaseInsensitiveDict()
    mock_request.body = MockBody() # Ensure .tell() exists
    mock_request.register_hook = MagicMock()
    mock_request._cookies = None # Used by extract_cookies_to_jar

    returned_request = auth(mock_request)

    # Assert that no Authorization header is set initially
    assert "Authorization" not in returned_request.headers

    # Assert that response hooks are registered
    returned_request.register_hook.assert_any_call("response", auth.handle_401)
    returned_request.register_hook.assert_any_call("response", auth.handle_redirect)

    # Assert thread local state is initialized
    assert hasattr(auth._thread_local, "init")
    assert auth._thread_local.init is True
    assert auth._thread_local.last_nonce == ""
    assert auth._thread_local.nonce_count == 0
    assert auth._thread_local.num_401_calls == 1
    assert auth._thread_local.pos == 0 # From mock_request.body.tell()

    # 2. Test handle_redirect
    mock_redirect_response = MagicMock(spec=Response)
    mock_redirect_response.status_code = 302
    mock_redirect_response.is_redirect = True
    mock_redirect_response.request = MagicMock(spec=Request) # Needed for _r.request = prep
    mock_redirect_response.request.body = MockBody() # Ensure .tell() exists

    # Ensure _thread_local.num_401_calls is not 1 initially to see the reset
    auth._thread_local.num_401_calls = 5

    # Call handle_redirect
    returned_response_after_redirect = auth.handle_redirect(mock_redirect_response)

    # Assert num_401_calls is reset to 1
    assert auth._thread_local.num_401_calls == 1
    # handle_redirect should return the original response object
    assert returned_response_after_redirect is mock_redirect_response