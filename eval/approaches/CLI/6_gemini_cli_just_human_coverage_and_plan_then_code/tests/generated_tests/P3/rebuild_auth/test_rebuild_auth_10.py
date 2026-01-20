from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request

def test_rebuild_auth_default_port_equivalence():
    s = Session()
    
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic Secret"
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com" # implicit port 80
    
    new_prep = prep.copy()
    new_prep.url = "http://hostA.com:80" # explicit port 80
    
    s.rebuild_auth(new_prep, resp)
    
    # Should not strip
    assert "Authorization" in new_prep.headers
