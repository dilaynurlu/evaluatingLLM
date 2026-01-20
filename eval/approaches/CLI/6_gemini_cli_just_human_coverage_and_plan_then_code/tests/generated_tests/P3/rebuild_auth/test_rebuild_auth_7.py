from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request

def test_rebuild_auth_http_to_https_allowed():
    s = Session()
    
    req = Request("GET", "http://hostA.com")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic Secret"
    
    resp = Response()
    resp.request = prep
    resp.url = "http://hostA.com"
    
    new_prep = prep.copy()
    new_prep.url = "https://hostA.com"
    
    s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" in new_prep.headers
    assert new_prep.headers["Authorization"] == "Basic Secret"
