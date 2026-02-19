from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_no_trust_env():
    session = Session()
    session.trust_env = False
    session.should_strip_auth = Mock(return_value=False)
    
    req = Mock()
    req.headers = {}
    req.url = "http://example.com/netrc"
    
    resp = Mock()
    resp.request.url = "http://example.com/old"
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        session.rebuild_auth(req, resp)
        mock_netrc.assert_not_called()
