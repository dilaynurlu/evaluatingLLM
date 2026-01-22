import pytest
from requests.auth import HTTPDigestAuth
from requests import Request, Response
from unittest.mock import Mock

def test_digest_auth_prevent_infinite_loop():
    """
    Test that handle_401 does not loop indefinitely if the server keeps rejecting the credentials.
    It should stop after 2 attempts (initial 401 -> retry -> 401 -> stop).
    """
    url = "http://example.org/loop"
    auth = HTTPDigestAuth("user", "wrongpass")
    
    req = Request("GET", url).prepare()
    auth(req) # Sets num_401_calls = 1
    
    # First 401 response
    resp1 = Response()
    resp1.status_code = 401
    resp1.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce1", qop="auth"'
    resp1.url = url
    resp1.request = req
    resp1._content = b""
    resp1.raw = Mock()
    resp1.connection = Mock()
    
    # The "retry" also returns a 401 (e.g., bad password)
    resp2 = Response()
    resp2.status_code = 401
    resp2.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce2", qop="auth"'
    resp2.url = url
    resp2._content = b""
    resp2.raw = Mock()
    resp2.connection = Mock()
    resp2.history = [resp1] # In real requests, history is populated
    
    resp1.connection.send.return_value = resp2

    # First call: should trigger a retry
    # Internal state: num_401_calls increments to 2
    result1 = auth.handle_401(resp1)
    
    assert result1 is resp2
    assert resp1.connection.send.call_count == 1
    
    # Now verify that passing resp2 to handle_401 does NOT trigger another send
    # because num_401_calls is 2, and the condition is (num_401_calls < 2)
    # The handle_401 method resets num_401_calls to 1 and returns the response as-is if limit reached.
    result2 = auth.handle_401(resp2)
    
    assert result2 is resp2
    assert resp2.connection.send.call_count == 0