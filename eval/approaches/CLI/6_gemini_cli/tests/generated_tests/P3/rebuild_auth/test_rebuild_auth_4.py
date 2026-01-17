from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request
from unittest.mock import patch

def test_rebuild_auth_no_netrc_if_untrusted():
    s = Session()
    s.trust_env = False
    
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostB.com"
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" not in new_prep.headers
    mock_netrc.assert_not_called() # Should not be called if trust_env is False? 
    # Wait, code: new_auth = get_netrc_auth(url) if self.trust_env else None
    # Yes.
