import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_retry_limit():
    """
    Test that HTTPDigestAuth limits the number of retries to prevent infinite loops.
    If the server keeps returning 401, it should stop after 2 attempts.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req) # Init state, num_401_calls = 1
    
    # Mock Connection
    adapter_mock = Mock(spec=HTTPAdapter)
    
    # Resp 1: The initial 401 from server
    r1 = Response()
    r1.status_code = 401
    r1.request = req
    r1._content = b""
    r1._content_consumed = True
    r1.headers["www-authenticate"] = 'Digest realm="r", nonce="n1", qop="auth"'
    r1.connection = adapter_mock
    
    # Resp 2: The response to the first retry (also 401)
    r2 = Response()
    r2.status_code = 401
    r2.request = req.copy()
    r2._content = b""
    r2._content_consumed = True
    r2.headers["www-authenticate"] = 'Digest realm="r", nonce="n2", qop="auth"'
    r2.connection = adapter_mock
    r2.history = [r1]

    # Configure adapter to return r2 when r1 is retried
    adapter_mock.send.return_value = r2
    
    # 1. Handle first 401. 
    # Current num_401_calls=1. 1 < 2 is True. Increments to 2. Retries. Returns r2.
    result1 = auth.handle_401(r1)
    assert result1 is r2
    assert adapter_mock.send.call_count == 1
    
    # 2. Handle second 401 (r2).
    # Current num_401_calls=2. 2 < 2 is False. Should NOT retry.
    result2 = auth.handle_401(r2)
    
    # Should just return r2 without calling send again
    assert result2 is r2
    assert adapter_mock.send.call_count == 1 # Still 1