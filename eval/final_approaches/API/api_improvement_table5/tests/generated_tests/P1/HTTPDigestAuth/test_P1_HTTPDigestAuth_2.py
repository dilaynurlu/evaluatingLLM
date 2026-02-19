import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_sha256():
    """
    Test Digest Auth using the SHA-256 algorithm.
    Ensures that the algorithm parameter is respected and reflected in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    url = "http://example.com/sha256"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    auth(req)
    
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req
    r_401._content = b""
    r_401._content_consumed = True
    
    # Challenge with algorithm=SHA-256
    nonce = "randomnonce"
    r_401.headers["www-authenticate"] = f'Digest realm="me", nonce="{nonce}", qop="auth", algorithm="SHA-256"'
    
    adapter_mock = Mock(spec=HTTPAdapter)
    r_success = Response()
    r_success.status_code = 200
    r_success._content = b""
    r_success.history = []
    adapter_mock.send.return_value = r_success
    r_401.connection = adapter_mock
    
    auth.handle_401(r_401)
    
    args, _ = adapter_mock.send.call_args
    sent_request = args[0]
    auth_header = sent_request.headers["Authorization"]
    
    assert 'algorithm="SHA-256"' in auth_header
    # For SHA-256, the response hash should be 64 hex characters (256 bits)
    # Extract the response="..." value
    import re
    match = re.search(r'response="([0-9a-f]+)"', auth_header)
    assert match is not None
    response_hash = match.group(1)
    assert len(response_hash) == 64