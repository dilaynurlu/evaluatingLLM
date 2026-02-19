import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_opaque_handling():
    """
    Test that the 'opaque' directive from the server challenge is echoed back
    verbatim in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req
    r_401._content = b""
    r_401._content_consumed = True
    
    opaque_val = "5ccc069c403ebaf9f0171e9517f40e41"
    r_401.headers["www-authenticate"] = f'Digest realm="r", nonce="n", qop="auth", opaque="{opaque_val}"'
    
    adapter_mock = Mock(spec=HTTPAdapter)
    adapter_mock.send.return_value = Response()
    adapter_mock.send.return_value._content = b""
    adapter_mock.send.return_value.history = []
    r_401.connection = adapter_mock
    
    auth.handle_401(r_401)
    
    args, _ = adapter_mock.send.call_args
    auth_header = args[0].headers["Authorization"]
    
    assert f'opaque="{opaque_val}"' in auth_header