from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        
def test_rebuild_auth_3():
    session = MockSession()
    
    prepared_request = Mock()
    prepared_request.url = "http://example.com/resource"
    prepared_request.headers = {} # No auth
    prepared_request.prepare_auth = Mock()
    
    response = Mock()
    response.request = Mock()
    response.request.url = "http://example.com/old"
    
    # Mock get_netrc_auth
    with patch('requests.sessions.get_netrc_auth', return_value=('user', 'pass')):
        session.rebuild_auth(prepared_request, response)
        
    prepared_request.prepare_auth.assert_called_with(('user', 'pass'))
