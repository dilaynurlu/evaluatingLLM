from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_rebuild_auth_2():
    # rebuild_auth: keep auth on same host
    s = Session()
    req = PreparedRequest()
    req.url = "http://example.com/bar"
    req.headers = {}
    req.headers["Authorization"] = "Basic secret"
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/foo"
    
    s.rebuild_auth(req, resp)
    assert "Authorization" in req.headers