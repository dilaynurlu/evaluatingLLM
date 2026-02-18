from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response
from unittest.mock import patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True

def test_rebuild_auth_3():
    # Test adding netrc auth
    session = MockSession()
    
    req = Request("GET", "http://example.com").prepare()
    
    resp = Response()
    resp.request = Request("GET", "http://other.com").prepare()
    
    # Mock get_netrc_auth
    with patch('requests.sessions.get_netrc_auth', return_value=('user', 'pass')):
        session.rebuild_auth(req, resp)
    
    # 'user', 'pass' -> Basic auth
    # Basic dXNlcjpwYXNz
    assert "Authorization" in req.headers
    assert req.headers["Authorization"].startswith("Basic ")
