import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_no_qop():
    """
    Test Digest Auth when 'qop' is missing from the server challenge (Legacy RFC 2069 mode).
    Expects that 'nc' and 'cnonce' fields are NOT present in the response header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/legacy")
    auth(req)
    
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req
    r_401._content = b""
    r_401._content_consumed = True
    
    # Challenge without 'qop'
    r_401.headers["www-authenticate"] = 'Digest realm="legacy", nonce="legacy_nonce"'
    
    adapter_mock = Mock(spec=HTTPAdapter)
    adapter_mock.send.return_value = Response()
    adapter_mock.send.return_value._content = b""
    adapter_mock.send.return_value.history = []
    r_401.connection = adapter_mock
    
    auth.handle_401(r_401)
    
    args, _ = adapter_mock.send.call_args
    auth_header = args[0].headers["Authorization"]
    
    # Should contain basic fields
    assert 'realm="legacy"' in auth_header
    assert 'nonce="legacy_nonce"' in auth_header
    assert 'response="' in auth_header
    
    # Should NOT contain qop-specific fields
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header