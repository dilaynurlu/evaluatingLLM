import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request
from unittest.mock import patch

def test_rebuild_auth_1():
    s = Session()
    s.auth = ("user", "pass")
    
    # Prep request with auth
    req = Request("GET", "http://example.com/foo", auth=("user", "pass"))
    prep = s.prepare_request(req)
    
    # Mock response that triggered redirect
    resp = Response()
    resp.request = prep
    resp.url = "http://example.com/foo"
    
    # Redirect to same host
    prep.url = "http://example.com/bar"
    
    s.rebuild_auth(prep, resp)
    
    assert "Authorization" in prep.headers
    assert prep.headers["Authorization"].startswith("Basic")
