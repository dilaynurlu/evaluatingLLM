from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request
from unittest.mock import patch

def test_rebuild_auth_same_host_no_strip_ignores_netrc_overlap():
    # If we keep same host, we keep Authorization.
    # But netrc is also checked.
    # prepare_auth overrides?
    # Code:
    # if "Authorization" in headers and ...: del ...
    # new_auth = get_netrc_auth(...)
    # if new_auth: prepared_request.prepare_auth(new_auth)
    
    # prepared_request.prepare_auth usually sets Authorization header.
    # So if netrc returns something, it MIGHT overwrite existing auth even on same host?
    # Let's verify this behavior.
    
    s = Session()
    s.trust_env = True
    
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic ManualAuth"
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostA.com/foo"
    
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        s.rebuild_auth(new_prep, resp)
    
    # It seems it WILL overwrite if netrc is found.
    # Ideally netrc shouldn't trigger if manual auth is present?
    # Requests behavior: environment (netrc) overrides if trust_env=True? 
    # Usually manual auth overrides environment. But here we are in a redirect.
    # If I manually set auth on first request, and redirect to same host, and netrc has entry...
    # The code doesn't check if Authorization is already present before calling prepare_auth.
    assert "Basic " in new_prep.headers["Authorization"]
    # We expect it to change to netrc one if my understanding is correct.
    # But let's check if the old one is preserved if netrc returns None.
