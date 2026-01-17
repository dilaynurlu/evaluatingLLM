import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_keeps_authorization_same_host():
    """
    Test that rebuild_auth retains the 'Authorization' header when redirecting
    to the same host.
    """
    session = Session()
    session.trust_env = False  # Disable netrc to ensure retention is due to host check
    
    # Original request context
    # Host: example.com
    original_req = Request("GET", "http://example.com/old_path", auth=("user", "pass")).prepare()
    
    response = Response()
    response.request = original_req
    
    # New request context
    # Host: example.com (same host -> should keep auth)
    new_url = "http://example.com/new_path"
    new_req = Request("GET", new_url).prepare()
    
    # Simulate header copy
    new_req.headers["Authorization"] = original_req.headers["Authorization"]
    original_auth_value = new_req.headers["Authorization"]
    
    # Call target function
    session.rebuild_auth(new_req, response)
    
    # Assert Authorization is preserved
    assert "Authorization" in new_req.headers
    assert new_req.headers["Authorization"] == original_auth_value