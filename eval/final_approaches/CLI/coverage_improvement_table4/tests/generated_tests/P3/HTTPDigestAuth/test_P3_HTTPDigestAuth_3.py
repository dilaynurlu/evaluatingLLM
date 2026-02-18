import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response, PreparedRequest
from requests.adapters import HTTPAdapter
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_simple():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    r = Mock(spec=Response)
    r.status_code = 401
    r.headers = {
        "www-authenticate": 'Digest realm="me@test.com", nonce="nonce", qop="auth"'
    }
    r.request = Mock(spec=PreparedRequest)
    r.request.copy.return_value = r.request
    r.request.headers = {}
    r.request.method = "GET"
    r.request.url = "http://localhost/"
    r.request.body = None
    r.content = b""
    r.raw = Mock()
    r.connection = Mock(spec=HTTPAdapter)
    
    # Return a success response on retry
    retry_response = Mock(spec=Response)
    retry_response.history = []
    retry_response.request = r.request
    r.connection.send.return_value = retry_response
    
    # Mock cookies
    r.request._cookies = Mock()
    
    result = auth.handle_401(r)
    
    assert result == retry_response
    assert "Authorization" in r.request.headers
    assert r.request.headers["Authorization"].startswith("Digest ")
