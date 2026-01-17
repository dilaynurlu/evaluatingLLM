import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_retry_limit():
    """
    Test that HTTPDigestAuth enforces a retry limit (num_401_calls).
    It should allow 2 attempts (initial 401 + 1 retry), then stop.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com").prepare()
    auth(req) # initializes internal state
    
    # First 401 Challenge
    r1 = Response()
    r1.status_code = 401
    r1.request = req
    r1.url = "http://example.com"
    r1._content = b""
    r1.headers["www-authenticate"] = 'Digest realm="r", nonce="n1", qop="auth"'
    r1.connection = Mock()
    
    # Response to the First Retry (also a 401)
    r2 = Response()
    r2.status_code = 401
    r2.request = req.copy()
    r2.url = "http://example.com"
    r2._content = b""
    r2.headers["www-authenticate"] = 'Digest realm="r", nonce="n2", qop="auth"'
    r2.connection = Mock()
    
    # Setup chain
    r1.connection.send.return_value = r2
    
    # 1. Handle first 401
    res1 = auth.handle_401(r1)
    
    # Expectation: A request was sent
    assert r1.connection.send.called
    assert res1 == r2
    assert auth._thread_local.num_401_calls == 2
    
    # 2. Handle second 401 (result of the retry)
    # The client has already retried once for this transaction (num_401_calls=2).
    # It should NOT retry again.
    res2 = auth.handle_401(r2)
    
    # Expectation: No request sent
    assert not r2.connection.send.called
    # Returns the response as-is
    assert res2 == r2
    # Counter should verify reset logic or max state
    assert auth._thread_local.num_401_calls == 1