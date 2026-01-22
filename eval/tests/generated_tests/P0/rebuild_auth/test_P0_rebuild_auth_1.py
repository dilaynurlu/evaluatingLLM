import requests
from requests.sessions import Session
from requests.models import Response, Request

def test_rebuild_auth_strips_authorization_on_redirect_to_different_host():
    session = Session()
    # Disable trust_env to prevent .netrc logic from interfering or re-adding auth
    session.trust_env = False
    
    # Original request (source of redirect)
    original_url = "http://example.com/source"
    original_req = Request("GET", original_url).prepare()
    
    # Response object that triggered the redirect
    response = Response()
    response.request = original_req
    
    # New request (target of redirect)
    # Simulating that headers were copied from original request before calling rebuild_auth
    target_url = "http://other-domain.com/target"
    auth_header_value = "Basic c2VjcmV0OnBhc3N3b3Jk"  # secret:password
    target_req = Request(
        "GET", 
        target_url, 
        headers={"Authorization": auth_header_value}
    ).prepare()
    
    # Verify pre-condition: Authorization header exists
    assert "Authorization" in target_req.headers
    
    # Execute the function under test
    session.rebuild_auth(target_req, response)
    
    # Verify post-condition: Authorization header should be removed due to host mismatch
    assert "Authorization" not in target_req.headers