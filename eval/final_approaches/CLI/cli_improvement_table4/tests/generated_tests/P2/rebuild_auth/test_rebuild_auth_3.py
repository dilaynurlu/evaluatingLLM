from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_netrc():
    session = Session()
    session.trust_env = True
    session.should_strip_auth = Mock(return_value=False)
    
    req = Mock()
    req.headers = {}
    req.url = "http://example.com/netrc"
    
    resp = Mock()
    resp.request.url = "http://example.com/old"
    
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")):
        session.rebuild_auth(req, resp)
    
    req.prepare_auth.assert_called_with(("user", "pass"))
