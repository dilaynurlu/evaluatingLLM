import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_retry_limit():
    """
    Test the retry limit for Digest Auth.
    Verifies that handle_401 does not resend the request if num_401_calls >= 2.
    """
    auth = HTTPDigestAuth("user", "pass")
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com")
    auth(request) # initializes num_401_calls = 1
    
    # Simulate that we have already retried once (so this is the second 401, entering with count=2 is tricky)
    # The logic is: if num_401_calls < 2: do retry.
    # If we manually set it to 2, it should assume we exceeded limit.
    auth._thread_local.num_401_calls = 2
    
    response = Response()
    response.status_code = 401
    response.request = request
    response.headers["www-authenticate"] = 'Digest realm="realm", nonce="new-nonce", qop="auth"'
    response._content = b""
    response.raw = Mock()
    
    # Mock connection to ensure it is NOT called
    response.connection = Mock()
    
    result = auth.handle_401(response)
    
    # Should return the original response without retrying
    assert result is response
    assert not response.connection.send.called
    
    # Verify counter is stuck or reset (logic sets it to 1 if returning invalid r, or keeps it if logic fail?)
    # Code:
    # if "digest" in ... and num_401_calls < 2: ... return _r
    # self._thread_local.num_401_calls = 1
    # return r
    # So if it falls through (condition fails), it resets to 1 and returns r.
    assert auth._thread_local.num_401_calls == 1