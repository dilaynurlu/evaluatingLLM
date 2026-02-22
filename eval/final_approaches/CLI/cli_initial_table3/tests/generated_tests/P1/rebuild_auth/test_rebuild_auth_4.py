from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock, patch

def test_rebuild_auth_no_netrc_untrusted():
    session = Session()
    session.trust_env = False
    session.should_strip_auth = MagicMock(return_value=False)
    
    # Prepared request without auth
    prep = PreparedRequest()
    prep.url = "http://example.com"
    prep.headers = {}
    
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        session.rebuild_auth(prep, Response())
        
        mock_netrc.assert_not_called()
        assert "Authorization" not in prep.headers
