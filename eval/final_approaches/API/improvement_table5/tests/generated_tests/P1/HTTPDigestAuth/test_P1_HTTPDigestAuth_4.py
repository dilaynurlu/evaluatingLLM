import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_md5_sess():
    """
    Test Digest Auth using the MD5-SESS algorithm.
    Verifies that the Authorization header indicates MD5-SESS.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/sess")
    auth(req)
    
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req
    r_401._content = b""
    r_401._content_consumed = True
    
    r_401.headers["www-authenticate"] = 'Digest realm="sess", nonce="xyz", qop="auth", algorithm="MD5-SESS"'
    
    adapter_mock = Mock(spec=HTTPAdapter)
    adapter_mock.send.return_value = Response()
    adapter_mock.send.return_value._content = b""
    adapter_mock.send.return_value.history = []
    r_401.connection = adapter_mock
    
    auth.handle_401(r_401)
    
    args, _ = adapter_mock.send.call_args
    auth_header = args[0].headers["Authorization"]
    
    assert 'algorithm="MD5-SESS"' in auth_header
    assert 'response="' in auth_header