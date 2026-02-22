from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        
def test_rebuild_auth_2():
    session = MockSession()
    
    prepared_request = Mock()
    prepared_request.url = "http://example.com/other"
    prepared_request.headers = {"Authorization": "Basic sensitive"}
    
    response = Mock()
    response.request = Mock()
    response.request.url = "http://example.com/resource"
    
    with patch.object(session, 'should_strip_auth', return_value=False):
        session.rebuild_auth(prepared_request, response)
        
    assert "Authorization" in prepared_request.headers
    assert prepared_request.headers["Authorization"] == "Basic sensitive"
