import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_sha512():
    """
    Test Digest Auth using the SHA-512 algorithm.
    Ensures that the algorithm parameter is respected and reflected in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    url = "http://example.com/sha512"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    auth(req)
    
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req
    r_401._content = b""
    r_401._content_consumed = True
    
    # Challenge with algorithm=SHA-512
    r_401.headers["www-authenticate"] = 'Digest realm="me", nonce="abc", qop="auth", algorithm="SHA-512"'
    
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
    
    assert 'algorithm="SHA-512"' in auth_header
    
    import re
    match = re.search(r'response="([0-9a-f]+)"', auth_header)
    assert match is not None
    response_hash = match.group(1)
    # SHA-512 produces 128 hex chars
    assert len(response_hash) == 128