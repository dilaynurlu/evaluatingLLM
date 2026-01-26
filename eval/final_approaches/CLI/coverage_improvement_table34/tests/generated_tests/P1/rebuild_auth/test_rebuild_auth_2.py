import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=True)

def test_rebuild_auth_strip():
    """Test that auth is stripped when should_strip_auth returns True."""
    session = MockSession()
    session.should_strip_auth.return_value = True
    
    prep = Mock()
    prep.headers = {"Authorization": "Basic 123"}
    prep.url = "http://other.com"
    
    response = Mock()
    response.request.url = "http://example.com"
    
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        session.rebuild_auth(prep, response)
    
    assert "Authorization" not in prep.headers
