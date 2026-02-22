from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = False
        
def test_rebuild_auth_5():
    session = MockSession()
    
    prepared_request = Mock()
    prepared_request.url = "http://example.com/resource"
    prepared_request.headers = {}
    prepared_request.prepare_auth = Mock()
    
    response = Mock()
    response.request = Mock()
    response.request.url = "http://example.com/old"
    
    # Even if get_netrc_auth returns something, it shouldn't be used if trust_env is False
    with patch('requests.sessions.get_netrc_auth', return_value=('user', 'pass')):
        session.rebuild_auth(prepared_request, response)
            
    prepared_request.prepare_auth.assert_not_called()
