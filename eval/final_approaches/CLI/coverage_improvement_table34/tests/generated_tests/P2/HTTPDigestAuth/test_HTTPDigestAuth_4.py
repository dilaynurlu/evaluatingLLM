from unittest.mock import Mock
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_handle_401_success():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Mock()
    r.status_code = 401
    r.headers = {"www-authenticate": 'Digest realm="me", nonce="123", qop="auth"'}
    r.request.url = "http://example.com/"
    r.request.copy.return_value = Mock()
    r.request.copy.return_value.method = "GET"

    r.request.copy.return_value.url = "http://example.com/"
    r.request.copy.return_value.headers = {}
    r.request.body = None
    
    mock_response = Mock()
    mock_response.history = []
    mock_response.request = Mock()
    r.connection.send.return_value = mock_response
    
    auth._thread_local.num_401_calls = 1
    res = auth.handle_401(r)
    
    assert res == mock_response
    assert auth._thread_local.nonce_count == 1
    assert auth._thread_local.chal["realm"] == "me"
    assert "Authorization" in r.request.copy.return_value.headers
