import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_handle_401():
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock response
    r = Mock()
    r.status_code = 401
    r.url = "http://example.com"
    r.request.url = "http://example.com"
    r.headers = {"www-authenticate": 'Digest realm="test", nonce="123", qop="auth"'}
    
    # Configure prepared request copy
    prep = Mock()
    prep.url = "http://example.com"
    prep.headers = {}
    prep._cookies = Mock() # Add _cookies mock if needed by extract_cookies
    r.request.copy.return_value = prep
    
    r.connection.send.return_value = Mock()
    r.content = b""
    
    # Initialize state
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    # Call handle_401
    new_resp = auth.handle_401(r)
    
    # Should have retried
    assert auth._thread_local.num_401_calls == 2
    assert r.connection.send.called
    assert new_resp != r
