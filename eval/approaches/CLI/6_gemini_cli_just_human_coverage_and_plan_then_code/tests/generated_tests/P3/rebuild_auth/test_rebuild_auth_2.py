from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request

def test_rebuild_auth_keep_same_host():
    s = Session()
    s.trust_env = False
    
    req = Request("GET", "http://hostA.com/path1")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic user:pass"
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com/path1"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostA.com/path2"
    
    s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" in new_prep.headers
    assert new_prep.headers["Authorization"] == "Basic user:pass"
