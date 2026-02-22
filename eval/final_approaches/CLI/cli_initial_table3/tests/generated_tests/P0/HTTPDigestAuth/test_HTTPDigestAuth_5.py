from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_5():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Mock()
    r.status_code = 401
    r.is_redirect = False
    r.headers = {
        "www-authenticate": 'Digest realm="me@kennethreitz.com", nonce="e921d7", algorithm="SHA-256", qop="auth"'
    }
    r.request = Mock()
    r.request.copy.return_value = r.request
    r.request.headers = {}
    r.request.method = "GET"
    r.request.url = "http://kennethreitz.com/digest-auth/auth/user/pass"
    r.request.path_url = "/digest-auth/auth/user/pass"
    r.content = b""
    r.close = Mock()
    r.raw = Mock()
    
    r.connection = Mock()
    success_response = Mock()
    success_response.status_code = 200
    success_response.history = []
    success_response.request = r.request
    r.connection.send.return_value = success_response

    auth._thread_local.num_401_calls = 1
    
    result = auth.handle_401(r)
    
    assert result == success_response
    auth_header = r.request.headers.get("Authorization")
    assert 'algorithm="SHA-256"' in auth_header
