import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=False)

@patch("requests.sessions.get_netrc_auth", return_value=None)
def test_rebuild_auth_verify_should_strip_args(mock_netrc):
    session = DummySession()
    
    request = Mock()
    request.headers = {"Authorization": "Basic old"}
    request.url = "http://new.example.com"
    
    response = Mock()
    response.request.url = "http://old.example.com"
    
    session.rebuild_auth(request, response)
    
    session.should_strip_auth.assert_called_with("http://old.example.com", "http://new.example.com")
