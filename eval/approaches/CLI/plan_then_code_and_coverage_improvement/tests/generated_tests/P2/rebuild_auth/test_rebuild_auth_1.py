from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_strip():
    session = Session()
    # mock should_strip_auth to return True
    session.should_strip_auth = Mock(return_value=True)
    
    req = Mock()
    req.headers = {"Authorization": "Basic 123"}
    req.url = "http://example.com/new"
    
    resp = Mock()
    resp.request.url = "http://example.com/old"
    
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        session.rebuild_auth(req, resp)
    
    assert "Authorization" not in req.headers
    session.should_strip_auth.assert_called_with("http://example.com/old", "http://example.com/new")
