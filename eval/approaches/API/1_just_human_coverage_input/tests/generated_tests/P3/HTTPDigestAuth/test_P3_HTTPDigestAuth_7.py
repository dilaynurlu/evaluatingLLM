import pytest
from unittest.mock import Mock, patch
import requests
from requests.auth import HTTPDigestAuth

def test_http_digest_auth_preemptive_nonce_reuse():
    """
    Test that HTTPDigestAuth reuses the last successful nonce to preemptively
    send the Authorization header on subsequent requests.
    """
    url = "http://example.org/resource"
    auth = HTTPDigestAuth("user", "pass")
    
    # 1. Setup a full successful flow to prime the auth state
    req1 = requests.Request("GET", url).prepare()
    resp_401 = requests.Response()
    resp_401.request = req1
    resp_401.url = url
    resp_401.status_code = 401
    resp_401.headers["www-authenticate"] = 'Digest realm="realm", nonce="prime_nonce", qop="auth"'
    resp_401._content = b""
    resp_401.raw = Mock()
    
    mock_connection = Mock()
    resp_success = requests.Response()
    resp_success.status_code = 200
    resp_success.request = req1
    mock_connection.send = Mock(return_value=resp_success)
    resp_401.connection = mock_connection
    
    # Run the flow
    auth(req1)
    auth.handle_401(resp_401)
    
    # Verify we authenticated once
    assert mock_connection.send.call_count == 1
    
    # 2. Create a NEW request to the same host
    req2 = requests.Request("GET", url).prepare()
    
    # 3. Call auth on the new request
    # This should detect the existing state for this thread/domain and apply headers immediately
    auth(req2)
    
    # 4. Assert Authorization header is present WITHOUT having received a 401 for req2
    auth_header = req2.headers.get("Authorization")
    assert auth_header is not None
    assert 'Digest ' in auth_header
    assert 'nonce="prime_nonce"' in auth_header
    # Check that it's a new request (nc might be 2 or reset depending on impl, but usually increments)
    # The default impl tracks nc.
    assert 'nc=' in auth_header