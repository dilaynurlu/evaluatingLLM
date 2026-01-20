import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=False)

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_netrc_apply(mock_netrc):
    mock_netrc.return_value = ("user", "pass")
    session = DummySession()
    
    request = Mock()
    request.headers = {}
    request.url = "http://example.com"
    request.prepare_auth = Mock()
    
    response = Mock()
    
    session.rebuild_auth(request, response)
    
    request.prepare_auth.assert_called_with(("user", "pass"))
