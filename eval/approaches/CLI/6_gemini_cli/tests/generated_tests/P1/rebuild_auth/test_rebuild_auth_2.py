import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=False)

@patch("requests.sessions.get_netrc_auth", return_value=None)
def test_rebuild_auth_keep_auth(mock_netrc):
    session = DummySession()
    
    request = Mock()
    request.headers = {"Authorization": "Basic old"}
    request.url = "http://same.example.com"
    request.prepare_auth = Mock()
    
    response = Mock()
    response.request.url = "http://same.example.com"
    
    session.rebuild_auth(request, response)
    
    assert request.headers["Authorization"] == "Basic old"
