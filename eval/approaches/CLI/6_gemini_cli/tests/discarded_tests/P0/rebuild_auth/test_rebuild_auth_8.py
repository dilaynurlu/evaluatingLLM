
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_https_to_http_allowed_same_host():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "https://example.com/bar"
    
    # https -> http same host allowed if ports are default
    session.rebuild_auth(req, resp)
    assert "Authorization" in req.headers
