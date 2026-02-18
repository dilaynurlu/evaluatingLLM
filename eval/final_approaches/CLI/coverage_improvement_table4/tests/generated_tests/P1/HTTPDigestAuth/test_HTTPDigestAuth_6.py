import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_success_flow():
    """Test handle_401 triggering a retry with digest auth."""
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1 # Initial call
    
    resp = Mock()
    resp.status_code = 401
    resp.headers = {"www-authenticate": 'Digest realm="test", nonce="123", qop="auth"'}
    resp.request.headers = {}
    resp.request.url = "http://example.com/"
    resp.request.copy = Mock(return_value=resp.request)
    resp.content = b"" # Consume content
    resp.close = Mock()
    resp.connection.send = Mock(return_value=Mock())
    resp.raw = Mock()
    resp.request._cookies = Mock() # needed for extract_cookies_to_jar
    
    # We need to mock extract_cookies_to_jar if it's called?
    # It is imported in auth.py. We might need to patch it if it fails on mocks.
    # But let's try with mocks first. 
    # _cookies being a Mock might fail if it expects a CookieJar.
    from requests.cookies import RequestsCookieJar
    resp.request._cookies = RequestsCookieJar()
    
    result = auth.handle_401(resp)
    
    # result is the new response from connection.send
    assert result == resp.connection.send.return_value
    assert "Authorization" in resp.request.headers
    assert resp.request.headers["Authorization"].startswith("Digest ")
