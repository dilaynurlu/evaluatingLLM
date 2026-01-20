from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request

def test_rebuild_auth_different_port_stripped():
    s = Session()
    
    req = Request("GET", "http://hostA.com:8080")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic Secret"
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com:8080"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostA.com:9090"
    
    s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" not in new_prep.headers
