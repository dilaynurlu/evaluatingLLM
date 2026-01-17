
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_http_to_https_allowed():
    session = Session()
    req = PreparedRequest()
    req.url = "https://example.com/foo"
    req.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/bar"
    
    # http -> https is special cased allowed if ports are default
    session.rebuild_auth(req, resp)
    assert "Authorization" in req.headers
