import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=False)

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_overwrite_existing(mock_netrc):
    mock_netrc.return_value = ("netrc_user", "netrc_pass")
    session = DummySession()
    
    request = Mock()
    request.headers = {"Authorization": "Basic existing"}
    request.url = "http://example.com"
    request.prepare_auth = Mock()
    
    response = Mock()
    response.request.url = "http://example.com"
    
    session.rebuild_auth(request, response)
    
    # It wasn't stripped, but prepare_auth is called, which usually overwrites.
    request.prepare_auth.assert_called_with(("netrc_user", "netrc_pass"))
