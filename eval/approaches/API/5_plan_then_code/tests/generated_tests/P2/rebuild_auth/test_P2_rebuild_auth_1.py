import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_authorization_different_host():
    """
    Test that rebuild_auth strips the 'Authorization' header when redirecting
    to a different host, provided trust_env is False (to ignore netrc).
    """
    session = Session()
    session.trust_env = False
    
    # Original request context (source of redirect)
    # Host: example.com
    original_req = Request("GET", "http://example.com/resource", auth=("user", "pass")).prepare()
    
    response = Response()
    response.request = original_req
    
    # New request context (target of redirect)
    # Host: other.com (different host -> should strip auth)
    new_url = "http://other.com/resource"
    new_req = Request("GET", new_url).prepare()
    
    # Simulate the behavior where headers are copied from original to new request
    # before rebuild_auth is called.
    new_req.headers["Authorization"] = original_req.headers["Authorization"]
    
    assert "Authorization" in new_req.headers
    
    # Call the target function
    session.rebuild_auth(new_req, response)
    
    # Assert Authorization is removed
    assert "Authorization" not in new_req.headers