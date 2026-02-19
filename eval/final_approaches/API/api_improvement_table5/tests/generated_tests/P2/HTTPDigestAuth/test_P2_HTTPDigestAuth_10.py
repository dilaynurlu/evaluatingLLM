import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_invalid_qop():
    """
    Test Digest Auth with an unsupported qop value.
    The implementation supports None or "auth". "auth-int" alone is not supported in the
    provided logic (unless "auth" is also present).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    # qop="auth-int" only (no "auth")
    resp.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth-int"'
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    handle_401_hook = req.hooks["response"][0]
    handle_401_hook(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    
    # build_digest_header returns None for unsupported qop
    assert sent_request.headers.get("Authorization") is None