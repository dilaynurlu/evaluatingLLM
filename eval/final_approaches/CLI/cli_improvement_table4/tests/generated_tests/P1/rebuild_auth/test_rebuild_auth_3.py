import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=False)

def test_rebuild_auth_netrc():
    """Test that netrc auth is applied if environment is trusted."""
    session = MockSession()
    session.trust_env = True
    
    prep = Mock()
    prep.headers = {}
    prep.url = "http://example.com"
    prep.prepare_auth = Mock()
    
    response = Mock()
    
    # Patch get_netrc_auth to return some auth
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")):
        session.rebuild_auth(prep, response)
    
    prep.prepare_auth.assert_called_with(("user", "pass"))
