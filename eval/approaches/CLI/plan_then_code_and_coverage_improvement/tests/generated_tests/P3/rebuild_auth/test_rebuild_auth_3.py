from requests.sessions import Session
from requests.models import Response, PreparedRequest
from unittest.mock import patch

def test_rebuild_auth_3():
    # rebuild_auth: new host, netrc has auth
    s = Session()
    s.trust_env = True
    req = PreparedRequest()
    req.url = "http://new-host.com/resource"
    req.headers = {}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://old-host.com/resource"
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        s.rebuild_auth(req, resp)
    
    assert "Authorization" in req.headers
    assert req.headers["Authorization"].startswith("Basic ")
