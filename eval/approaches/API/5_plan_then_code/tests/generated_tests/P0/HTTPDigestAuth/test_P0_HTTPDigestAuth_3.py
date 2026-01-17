import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication with SHA-256 algorithm.
    Verifies that the generated header correctly includes 'algorithm="SHA-256"'
    and utilizes SHA-256 for the hash generation.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    resp = Response()
    resp.request = req
    resp.status_code = 401
    # Challenge specifying SHA-256
    resp.headers["www-authenticate"] = 'Digest realm="me", nonce="123", qop="auth", algorithm="SHA-256"'
    resp._content = b""
    resp.raw = Mock()
    
    mock_send = Mock()
    mock_send.return_value = Response()
    resp.connection = Mock()
    resp.connection.send = mock_send

    with patch("requests.auth.os.urandom", return_value=b"123"), \
         patch("requests.auth.time.ctime", return_value="time"):
        
        auth.handle_401(resp)
        
        assert mock_send.called
        sent_req = mock_send.call_args[0][0]
        auth_header = sent_req.headers["Authorization"]
        
        assert 'algorithm="SHA-256"' in auth_header
        # The response field is a hash. For SHA-256, it should be 64 hex characters.
        # Format: response="..."
        # We can extract it roughly.
        import re
        match = re.search(r'response="([^"]+)"', auth_header)
        assert match is not None
        response_hash = match.group(1)
        assert len(response_hash) == 64  # SHA-256 hexdigest length