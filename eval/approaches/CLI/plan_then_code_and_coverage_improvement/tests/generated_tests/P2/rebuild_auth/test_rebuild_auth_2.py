from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_retain():
    session = Session()
    session.should_strip_auth = Mock(return_value=False)
    
    req = Mock()
    req.headers = {"Authorization": "Basic 123"}
    req.url = "http://example.com/new"
    
    resp = Mock()
    resp.request.url = "http://example.com/old"
    
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        session.rebuild_auth(req, resp)
    
    assert req.headers["Authorization"] == "Basic 123"
