import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=True)

@patch("requests.sessions.get_netrc_auth", return_value=None)
def test_rebuild_auth_no_header(mock_netrc):
    session = DummySession()
    
    request = Mock()
    request.headers = {}
    request.url = "http://new.example.com"
    
    response = Mock()
    response.request.url = "http://old.example.com"
    
    session.rebuild_auth(request, response)
    
    assert "Authorization" not in request.headers
