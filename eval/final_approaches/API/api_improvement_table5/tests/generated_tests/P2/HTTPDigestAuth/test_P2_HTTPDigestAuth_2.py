import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Auth with algorithm="SHA-256".
    Verifies that the correct hashing algorithm is detected and used.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/api")
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    # Challenge specifying SHA-256
    resp.headers["www-authenticate"] = (
        'Digest realm="sha256realm", nonce="randomnonce", '
        'qop="auth", algorithm="SHA-256"'
    )
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    handle_401_hook = req.hooks["response"][0]
    handle_401_hook(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'response="' in auth_header
    
    # SHA-256 hex digest is 64 characters long
    # Extract response value
    import re
    match = re.search(r'response="([^"]+)"', auth_header)
    assert match
    response_hash = match.group(1)
    assert len(response_hash) == 64