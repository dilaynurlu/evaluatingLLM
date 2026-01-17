
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_keep_same_host():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/bar"
    
    session.rebuild_auth(req, resp)
    assert "Authorization" in req.headers
    assert req.headers["Authorization"] == "Basic dXNlcjpwYXNz"
