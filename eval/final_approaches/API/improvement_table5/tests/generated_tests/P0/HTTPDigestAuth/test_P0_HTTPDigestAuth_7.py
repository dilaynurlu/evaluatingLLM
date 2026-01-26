import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_retry_limit():
    """
    Test that handle_401 stops retrying after 2 attempts to prevent infinite recursion
    if the server keeps rejecting credentials.
    """
    auth = HTTPDigestAuth("user", "pass")
    request = Request("GET", "http://example.com/").prepare()
    auth(request)
    
    # First 401 (Attempt 1)
    r1 = Response()
    r1.status_code = 401
    r1.request = request
    r1.headers["www-authenticate"] = 'Digest realm="test", nonce="nonce1"'
    r1._content = b""
    r1.raw = Mock()
    r1.connection = Mock()
    
    # Mock send to return ANOTHER 401 (Attempt 2 failure)
    r2 = Response()
    r2.status_code = 401
    r2.request = request
    r2.history = [r1]
    r2.headers["www-authenticate"] = 'Digest realm="test", nonce="nonce1"'
    r2._content = b""
    r2.raw = Mock()
    r2.connection = Mock()
    
    r1.connection.send.return_value = r2
    
    # Handle first 401 -> Should retry
    res1 = auth.handle_401(r1)
    assert res1 is r2
    assert r1.connection.send.call_count == 1
    # Check internal counter
    assert auth._thread_local.num_401_calls == 2
    
    # Handle second 401 (r2) -> Should NOT retry because num_401_calls is 2
    res2 = auth.handle_401(r2)
    
    # Should return original r2 without calling send
    assert res2 is r2
    assert r2.connection.send.call_count == 0