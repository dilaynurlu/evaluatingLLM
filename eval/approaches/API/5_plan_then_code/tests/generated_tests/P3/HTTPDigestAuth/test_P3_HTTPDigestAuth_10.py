import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_ignore_non_401():
    """
    Test that handle_401 ignores responses with status codes other than 401
    (e.g., 200 OK or 404 Not Found), returning them as-is without modification
    or side effects on the retry counter.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com").prepare()
    auth(req)
    
    # Dirty the state to ensure it resets or stays consistent
    auth._thread_local.num_401_calls = 2
    
    response = Response()
    response.status_code = 200
    response.request = req
    # Even if www-authenticate header is present (weird but possible), it should be ignored if not 401
    response.headers["www-authenticate"] = 'Digest realm="r", nonce="n"'
    
    response.connection = Mock()
    
    result = auth.handle_401(response)
    
    assert result == response
    assert not response.connection.send.called
    # Assert state reset implies success
    assert auth._thread_local.num_401_calls == 1