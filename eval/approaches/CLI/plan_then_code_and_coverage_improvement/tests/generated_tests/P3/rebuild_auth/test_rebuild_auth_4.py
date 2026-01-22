from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_rebuild_auth_4():
    # trust_env = False -> should not look up netrc
    s = Session()
    s.trust_env = False
    
    req = PreparedRequest()
    req.url = "http://new-host.com/resource"
    req.headers = {}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://old-host.com/resource"
    
    # Even if netrc has auth, it shouldn't be used
    # We can patch get_netrc_auth to fail if called
    from unittest.mock import patch
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        s.rebuild_auth(req, resp)
        mock_netrc.assert_not_called()
    
    assert "Authorization" not in req.headers
