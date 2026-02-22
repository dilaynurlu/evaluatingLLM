import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request

def test_rebuild_auth_2():
    s = Session()
    
    # Original request with auth
    req = Request("GET", "http://example.com/foo", auth=("user", "pass"))
    original_prep = s.prepare_request(req)
    
    # Mock response referencing original request
    resp = Response()
    resp.request = original_prep
    resp.url = "http://example.com/foo"
    
    # New request (redirected)
    # We copy logic from resolve_redirects: it copies the request and changes URL
    new_prep = original_prep.copy()
    new_prep.url = "http://other.com/bar"
    
    s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" not in new_prep.headers
