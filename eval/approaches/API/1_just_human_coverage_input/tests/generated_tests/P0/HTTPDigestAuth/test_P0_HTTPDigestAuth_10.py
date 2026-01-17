import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_http_digest_auth_unknown_algorithm():
    """
    Test handling of a challenge with an unknown algorithm.
    The build_digest_header method returns None, so no Authorization header is generated.
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
    # Unknown algorithm
    resp.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="123", algorithm="UNKNOWN_ALGO"'
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
    
    # If build_digest_header returns None, header is set to None.
    args, _ = resp.connection.send.call_args
    sent_request = args[0]
    
    # requests allows setting header to None (which usually removes it or sends nothing),
    # but strictly checking that logic:
    assert sent_request.headers.get("Authorization") is None