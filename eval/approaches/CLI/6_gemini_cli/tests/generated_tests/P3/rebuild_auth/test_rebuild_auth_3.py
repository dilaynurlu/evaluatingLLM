from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request
from unittest.mock import patch

def test_rebuild_auth_load_netrc():
    s = Session()
    s.trust_env = True
    
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    # No initial auth
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostB.com"
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" in new_prep.headers
    # Basic auth string for netrc_user:netrc_pass
    assert "Basic " in new_prep.headers["Authorization"]
