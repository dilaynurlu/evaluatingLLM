import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_limit_401_retries():
    """
    Test that the authentication handler gives up after 2 attempts to avoid infinite loops.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = requests.Request("GET", "http://example.com").prepare()
    resp = requests.Response()
    resp.status_code = 401
    resp.request = req
    resp.headers = {"www-authenticate": 'Digest realm="r", nonce="n"'}
    resp._content = b""
    resp.connection = Mock()
    resp.raw = Mock()
    
    # Initialize state
    auth(req)
    
    # Artificially set attempts to 2 (limit)
    auth._thread_local.num_401_calls = 2
    
    # Call handler
    result = auth.handle_401(resp)
    
    # Should return original response (failure) without retrying
    assert result is resp
    assert resp.connection.send.called is False
    # Counter should be reset after failure
    assert auth._thread_local.num_401_calls == 1