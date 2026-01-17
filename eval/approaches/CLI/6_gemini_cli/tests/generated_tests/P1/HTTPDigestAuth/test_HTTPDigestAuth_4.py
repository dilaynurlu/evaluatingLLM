import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from unittest.mock import Mock

def test_HTTPDigestAuth_handle_401_success():
    auth = HTTPDigestAuth("user", "pass")
    
    # Use real Response and PreparedRequest to avoid mock attribute issues
    r = Response()
    r.status_code = 401
    r.headers = {"www-authenticate": 'Digest realm="realm", nonce="nonce", qop="auth"'}
    r.request = PreparedRequest()
    r.request.url = "http://example.com/"
    r.request.method = "GET"
    r.request.body = None
    r.request.headers = CaseInsensitiveDict() # Must initialize headers
    r.connection = Mock()
    r._content = b"" # Consume content
    
    # Mock the resent response
    new_response = Response()
    new_response.status_code = 200
    r.connection.send.return_value = new_response
    
    # Initialize state (usually done in __call__)
    auth.init_per_thread_state()
    auth._thread_local.pos = None
    auth._thread_local.num_401_calls = 1
    
    result = auth.handle_401(r)
    
    assert result == new_response
    # Verify we sent a new request
    assert r.connection.send.called
    args, kwargs = r.connection.send.call_args
    prepared_request = args[0]
    assert "Authorization" in prepared_request.headers
    assert prepared_request.headers["Authorization"].startswith("Digest ")
