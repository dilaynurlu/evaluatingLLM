import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_flow_md5():
    """
    Test standard MD5 Digest Authentication flow with qop='auth'.
    Verifies that a 401 response triggers a retry with the correct Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create the request that triggered the 401
    url = "http://example.org/resource"
    req = requests.Request("GET", url).prepare()
    
    # Create the 401 response
    resp = requests.Response()
    resp.status_code = 401
    resp.url = url
    resp.request = req
    resp.headers = {
        "www-authenticate": 'Digest realm="testrealm", nonce="nonce123", qop="auth", opaque="opaqueVal"'
    }
    resp._content = b""  # Empty content to simulate consumed response
    
    # Mock connection and its send method to return a 200 OK on retry
    resp.connection = Mock()
    resp.raw = Mock()
    
    retry_resp = requests.Response()
    retry_resp.status_code = 200
    retry_resp.request = req
    retry_resp.history = [resp]
    
    resp.connection.send.return_value = retry_resp
    
    # Initialize thread local state
    auth(req)
    
    # Trigger the 401 handler
    result = auth.handle_401(resp)
    
    # Verification
    assert result.status_code == 200
    assert resp.connection.send.call_count == 1
    
    # Inspect the prepared request sent in the retry
    args, _ = resp.connection.send.call_args
    sent_request = args[0]
    auth_header = sent_request.headers["Authorization"]
    
    # Validate Header Components
    assert auth_header.startswith("Digest ")
    assert 'username="user"' in auth_header
    assert 'realm="testrealm"' in auth_header
    assert 'nonce="nonce123"' in auth_header
    assert 'uri="/resource"' in auth_header
    assert 'qop="auth"' in auth_header
    assert 'nc=00000001' in auth_header
    assert 'opaque="opaqueVal"' in auth_header
    # response and cnonce are generated dynamic hashes; we just check presence
    assert 'response="' in auth_header
    assert 'cnonce="' in auth_header