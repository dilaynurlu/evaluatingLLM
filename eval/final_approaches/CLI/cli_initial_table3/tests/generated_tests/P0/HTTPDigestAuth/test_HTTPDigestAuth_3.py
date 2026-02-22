from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_3():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    # Mock Response and Request
    r = Mock()
    r.status_code = 401
    r.is_redirect = False
    r.headers = {
        "www-authenticate": 'Digest realm="me@kennethreitz.com", nonce="e921d7", algorithm="MD5", qop="auth"'
    }
    r.request = Mock()
    r.request.copy.return_value = r.request
    r.request.headers = {}
    r.request.method = "GET"
    r.request.url = "http://kennethreitz.com/digest-auth/auth/user/pass"
    # path_url is usually /path?query
    r.request.path_url = "/digest-auth/auth/user/pass"
    r.content = b""
    r.close = Mock()
    r.raw = Mock()
    
    # Mock connection.send
    r.connection = Mock()
    success_response = Mock()
    success_response.status_code = 200
    success_response.history = []
    success_response.request = r.request
    r.connection.send.return_value = success_response

    # Force num_401_calls < 2
    auth._thread_local.num_401_calls = 1
    
    # Call handle_401
    # Note: handle_401 calls self.build_digest_header which uses thread_local state
    result = auth.handle_401(r)
    
    # Verify
    assert result == success_response
    auth_header = r.request.headers.get("Authorization")
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    assert 'username="user"' in auth_header
    assert 'realm="me@kennethreitz.com"' in auth_header
    assert 'nonce="e921d7"' in auth_header
    assert 'uri="/digest-auth/auth/user/pass"' in auth_header
    assert 'response="' in auth_header
    assert 'algorithm="MD5"' in auth_header
