import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from unittest.mock import Mock

def test_HTTPDigestAuth_complex_header_parsing():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    r = Mock(spec=Response)
    r.status_code = 401
    # Complex header with quoted commas
    r.headers = {
        "www-authenticate": 'Digest realm="me@test.com", nonce="nonce,with,comma", qop="auth,auth-int", opaque="val,ue"'
    }
    r.request = Mock(spec=PreparedRequest)
    r.request.copy.return_value = r.request
    r.request.headers = {}
    r.request.method = "GET"
    r.request.url = "http://localhost/"
    r.request.body = None
    r.content = b""
    r.raw = Mock()
    r.connection = Mock()
    
    # We just want to check parsing logic
    # Mock connection.send to return success
    success = Mock(spec=Response)
    success.history = []
    success.request = r.request
    r.connection.send.return_value = success
    
    # Mock cookies
    r.request._cookies = Mock()
    
    auth.handle_401(r)
    
    # Check if parsed correctly
    chal = auth._thread_local.chal
    assert chal["realm"] == "me@test.com"
    assert chal["nonce"] == "nonce,with,comma"
    assert chal["qop"] == "auth,auth-int"
    assert chal["opaque"] == "val,ue"
