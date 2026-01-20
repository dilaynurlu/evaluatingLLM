import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = False # Disable env trust
        self.should_strip_auth = Mock(return_value=False)

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_netrc_no_trust(mock_netrc):
    session = DummySession()
    
    request = Mock()
    request.headers = {}
    request.url = "http://example.com"
    request.prepare_auth = Mock()
    
    response = Mock()
    
    session.rebuild_auth(request, response)
    
    assert not mock_netrc.called
    assert not request.prepare_auth.called
