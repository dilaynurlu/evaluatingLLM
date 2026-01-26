import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = False # Untrusted
        self.should_strip_auth = Mock(return_value=False)

def test_rebuild_auth_no_netrc_untrusted():
    """Test that netrc auth is NOT applied if environment is untrusted."""
    session = MockSession()
    session.trust_env = False
    
    prep = Mock()
    prep.headers = {}
    prep.url = "http://example.com"
    prep.prepare_auth = Mock()
    
    response = Mock()
    
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")):
        session.rebuild_auth(prep, response)
    
    prep.prepare_auth.assert_not_called()
