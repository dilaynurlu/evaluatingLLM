
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_changed_port_same_host():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com:8080/foo"
    req.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com:9090/bar"
    
    # Different port -> should strip auth (unless default ports, which these aren't)
    session.rebuild_auth(req, resp)
    assert "Authorization" not in req.headers
