import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_http_digest_auth_handle_401_sha256():
    """
    Test handling of a 401 response with a SHA-256 Digest challenge.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.org/"
    req.headers = {}
    req.hooks = {"response": []}
    
    auth(req)
    
    resp = Mock(spec=Response)
    resp.request = req
    resp.status_code = 401
    resp.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="123", qop="auth", algorithm="SHA-256"'
    }
    resp.content = b""
    resp.raw = Mock()
    resp.raw._original_response = None
    resp.is_redirect = False
    resp.connection = Mock()
    
    retry_resp = Mock(spec=Response)
    retry_resp.history = []
    resp.connection.send.return_value = retry_resp
    
    auth.handle_401(resp)
    
    args, _ = resp.connection.send.call_args
    sent_request = args[0]
    auth_header = sent_request.headers.get("Authorization")
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'response="' in auth_header