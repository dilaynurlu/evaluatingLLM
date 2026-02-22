from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock, patch

def test_rebuild_auth_netrc():
    session = Session()
    session.trust_env = True
    session.should_strip_auth = MagicMock(return_value=False)
    
    # Prepared request without auth
    prep = PreparedRequest()
    prep.url = "http://example.com"
    prep.headers = {}
    
    # Mock get_netrc_auth
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        mock_netrc.return_value = ("user", "pass")
        
        # We need `prepare_auth` to be called.
        # PreparedRequest.prepare_auth is real, let's mock it on the instance or check headers.
        # But `prepare_auth` modifies headers.
        
        session.rebuild_auth(prep, Response())
        
        # Check if auth was applied (basic auth usually)
        assert "Authorization" in prep.headers
        assert prep.headers["Authorization"].startswith("Basic ")
        mock_netrc.assert_called_with("http://example.com")
