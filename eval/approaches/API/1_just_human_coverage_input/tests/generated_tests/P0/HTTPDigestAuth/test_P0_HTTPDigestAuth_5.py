import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_http_digest_auth_opaque_handling():
    """
    Test that the 'opaque' directive from the server challenge is reflected back
    in the Authorization header.
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
        "www-authenticate": 'Digest realm="realm", nonce="123", opaque="secretdata", algorithm="MD5"'
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
    
    assert 'opaque="secretdata"' in auth_header