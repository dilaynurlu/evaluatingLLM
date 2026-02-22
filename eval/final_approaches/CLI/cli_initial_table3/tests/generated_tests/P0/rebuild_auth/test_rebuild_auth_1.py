from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        
def test_rebuild_auth_1():
    session = MockSession()
    
    # Mock prepared_request (the new request)
    prepared_request = Mock()
    prepared_request.url = "http://evil.com/resource"
    prepared_request.headers = {"Authorization": "Basic sensitive"}
    
    # Mock response (the original request)
    response = Mock()
    response.request = Mock()
    response.request.url = "http://example.com/resource"
    
    # Mock should_strip_auth to return True (different host)
    with patch.object(session, 'should_strip_auth', return_value=True):
        session.rebuild_auth(prepared_request, response)
        
    assert "Authorization" not in prepared_request.headers
