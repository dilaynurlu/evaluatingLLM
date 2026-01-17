import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication using SHA-256 algorithm.
    Verifies that the correct hashing algorithm is selected and indicated in the header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    url = "http://example.org/secure"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    
    resp = Response()
    resp.status_code = 401
    # Challenge specifies SHA-256
    resp.headers["www-authenticate"] = 'Digest realm="sha256realm", nonce="shanonce", algorithm="SHA-256", qop="auth"'
    resp.request = req
    resp._content = b""
    
    mock_connection = Mock()
    mock_connection.send.return_value = Response()
    resp.connection = mock_connection
    
    auth(req)
    
    # Deterministic mocks
    with patch("os.urandom", return_value=b"random"), \
         patch("time.ctime", return_value="TimeStr"):
         
        auth.handle_401(resp)
        
    retry_req = mock_connection.send.call_args[0][0]
    auth_header = retry_req.headers["Authorization"]
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'nonce="shanonce"' in auth_header
    
    # Verify response hash length (SHA-256 hex digest is 64 chars)
    # Extract response="<hash>"
    import re
    match = re.search(r'response="([a-f0-9]+)"', auth_header)
    assert match is not None
    response_hash = match.group(1)
    assert len(response_hash) == 64