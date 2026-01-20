from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request
from unittest.mock import patch, Mock

def test_rebuild_auth_strip_cross_host():
    s = Session()
    s.trust_env = False # Disable netrc for this test
    
    # Original request to host A
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic user:pass"
    
    # Response from host A redirecting to host B
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com"
    
    # New prepared request to host B
    new_prep = prep.copy()
    new_prep.url = "http://hostB.com"
    
    s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" not in new_prep.headers
