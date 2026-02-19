import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_retry_limit():
    """
    Test that handle_401 stops retrying after 2 attempts to avoid infinite loops.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    # Manually set the num_401_calls to limit (2)
    # Note: auth(req) sets it to 1. We must override it after auth(req) call.
    auth._thread_local.num_401_calls = 2
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", qop="auth"'
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    
    handle_401_hook = req.hooks["response"][0]
    
    # Trigger hook
    result = handle_401_hook(resp)
    
    # Assert that NO new request was sent
    assert not mock_connection.send.called
    
    # Assert that it returns the original response
    assert result is resp
    
    # Assert counter didn't increment past limit check logic (or stayed at 2)
    # The logic is: if ... num_401_calls < 2: ... else: num_401_calls = 1; return r
    assert auth._thread_local.num_401_calls == 1