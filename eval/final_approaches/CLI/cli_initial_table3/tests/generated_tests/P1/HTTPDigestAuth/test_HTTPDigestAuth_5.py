import io
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from unittest.mock import MagicMock, patch

def test_HTTPDigestAuth_retry_limit():
    auth = HTTPDigestAuth("user", "passwd")
    
    # Mock Response with 401
    r = Response()
    r.status_code = 401
    r.url = "http://example.com/foo"
    r.headers = {"www-authenticate": 'Digest realm="testrealm", nonce="12345", algorithm="MD5", qop="auth"'}
    r.raw = io.BytesIO(b"")
    r.reason = "Unauthorized"
    r.encoding = "utf-8"
    
    # Mock request associated with response
    req = Request('GET', 'http://example.com/foo')
    r.request = req.prepare()
    r.request.body = None 
    
    # Mock connection
    r.connection = MagicMock()
    
    # Initialize thread local state
    auth(r.request) 
    
    # Simulate first failure
    auth.handle_401(r)
    
    # Check if retry occurred
    assert r.connection.send.call_count == 1
    
    # Now assume the retried response is ALSO 401
    # We simulate this by calling handle_401 again on the new response
    # Or just reuse r but mock that it came from the retry
    
    # The implementation increments `_thread_local.num_401_calls`.
    # It starts at 1 (init by `__call__`).
    # handle_401 checks `if ... num_401_calls < 2`.
    
    # First call: num_401_calls becomes 2. Sends retry.
    # Second call (on retry response): num_401_calls is 2. Should NOT send retry.
    
    # Reset mock for clarity
    r.connection.send.reset_mock()
    
    # Call handle_401 again (simulating 401 on the retry)
    # The auth object state persists in thread local storage
    
    # Mock extract_cookies_to_jar
    with patch('requests.auth.extract_cookies_to_jar'):
        result = auth.handle_401(r)
    
    # Verify NO new request was sent
    assert r.connection.send.call_count == 0
    # Result should be the original response (r) because we gave up
    assert result == r
