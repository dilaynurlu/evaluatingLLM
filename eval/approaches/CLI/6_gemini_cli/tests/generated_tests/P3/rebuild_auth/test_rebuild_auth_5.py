from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request
from unittest.mock import patch

def test_rebuild_auth_strip_then_netrc():
    # Test that we strip old auth but apply new netrc auth if available
    s = Session()
    s.trust_env = True
    
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    prep.headers["Authorization"] = "OldAuth"
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostB.com"
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        s.rebuild_auth(new_prep, resp)
    
    assert new_prep.headers["Authorization"] != "OldAuth"
    assert "Basic " in new_prep.headers["Authorization"]
