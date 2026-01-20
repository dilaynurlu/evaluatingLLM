
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strip_different_host():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://original.com/bar"
    
    session.rebuild_auth(req, resp)
    assert "Authorization" not in req.headers
