import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_invalid_algo():
    """
    Test behavior when the server proposes an unsupported algorithm.
    The client should NOT send an Authorization header or retry the request.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.request = req
    response.url = "http://example.com"
    response._content = b""
    # Unsupported algorithm
    response.headers["www-authenticate"] = 'Digest realm="r", nonce="n", algorithm="ALIEN-HASH"'
    
    response.connection = Mock()
    
    # Action
    # Implementation detail: handle_401 returns the response if it can't handle the auth
    # or if it decides not to retry.
    result = auth.handle_401(response)
    
    # Assertions
    # 1. Connection.send should NOT be called (no retry)
    assert not response.connection.send.called
    # 2. Original response returned
    assert result == response