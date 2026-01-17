import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import Request, Response

def test_digest_auth_retry_limit_enforcement():
    """
    Test that handle_401 enforces a limit on the number of retries.
    If the limit (2) is reached, it should return the original 401 response
    instead of attempting another Digest handshake.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.org/loop").prepare()
    
    # Initialize
    auth(req)
    
    # Artificially set the retry counter to the limit
    # Accessing internal thread local storage for test setup
    auth._thread_local.num_401_calls = 2
    
    response = Response()
    response.status_code = 401
    response.url = "http://example.org/loop"
    response.request = req
    response.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    response._content = b""
    response.raw = Mock()
    
    mock_connection = Mock()
    response.connection = mock_connection
    
    # Trigger handle_401
    result = auth.handle_401(response)
    
    # Assert that no new request was sent
    assert not mock_connection.send.called
    
    # Assert that the original response object is returned
    assert result is response