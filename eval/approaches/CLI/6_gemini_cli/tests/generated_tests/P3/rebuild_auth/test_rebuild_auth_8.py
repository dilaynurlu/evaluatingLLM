from requests.sessions import Session
from requests.models import Response, PreparedRequest, Request

def test_rebuild_auth_https_to_http_stripped():
    s = Session()
    
    req = Request("GET", "https://hostA.com")
    prep = req.prepare()
    prep.headers["Authorization"] = "Basic Secret"
    
    resp = Response()
    resp.request = prep
    resp.url = "https://hostA.com"
    
    new_prep = prep.copy()
    new_prep.url = "http://hostA.com"
    
    s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" not in new_prep.headers
