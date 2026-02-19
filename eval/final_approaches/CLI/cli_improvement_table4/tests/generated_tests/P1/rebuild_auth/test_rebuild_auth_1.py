import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, patch

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
        self.should_strip_auth = Mock(return_value=False)
        self.prepare_auth = Mock() # Session doesn't have prepare_auth? 
        # Wait, rebuild_auth calls prepared_request.prepare_auth(new_auth)
        # So prepared_request needs prepare_auth.

def test_rebuild_auth_no_strip():
    """Test that auth is preserved when should_strip_auth returns False."""
    session = MockSession()
    session.should_strip_auth.return_value = False
    
    prep = Mock()
    prep.headers = {"Authorization": "Basic 123"}
    prep.url = "http://example.com"
    
    response = Mock()
    response.request.url = "http://example.com"
    
    # Patch get_netrc_auth to return None
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        session.rebuild_auth(prep, response)
    
    assert "Authorization" in prep.headers
    assert prep.headers["Authorization"] == "Basic 123"
