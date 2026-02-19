import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_unknown_algorithm():
    """
    Test Digest Auth with an unknown/unsupported algorithm.
    Should result in build_digest_header returning None, and Authorization header being None.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    # Unknown algorithm
    resp.headers["www-authenticate"] = (
        'Digest realm="r", nonce="n", qop="auth", algorithm="UNKNOWN-ALGO"'
    )
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    handle_401_hook = req.hooks["response"][0]
    handle_401_hook(resp)
    
    # Verify request sent
    sent_request = mock_connection.send.call_args[0][0]
    
    # Authorization header should be None or missing because build_digest_header returns None
    # and req.headers['Authorization'] = None usually removes it.
    assert sent_request.headers.get("Authorization") is None