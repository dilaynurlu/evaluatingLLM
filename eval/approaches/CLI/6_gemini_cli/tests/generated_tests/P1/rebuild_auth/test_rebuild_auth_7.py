import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=True)

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_strip_and_netrc(mock_netrc):
    mock_netrc.return_value = ("new_user", "new_pass")
    session = DummySession()
    
    request = Mock()
    request.headers = {"Authorization": "Basic old"}
    request.url = "http://new.example.com"
    request.prepare_auth = Mock()
    
    response = Mock()
    response.request.url = "http://old.example.com"
    
    session.rebuild_auth(request, response)
    
    assert "Authorization" not in request.headers
    request.prepare_auth.assert_called_with(("new_user", "new_pass"))
