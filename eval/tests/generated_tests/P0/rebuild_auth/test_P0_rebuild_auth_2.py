import requests
from requests.sessions import Session
from requests.models import Response, Request

def test_rebuild_auth_keeps_authorization_on_redirect_to_same_host():
    session = Session()
    session.trust_env = False
    
    # Original request to the same host
    host = "http://example.com"
    original_url = f"{host}/source"
    original_req = Request("GET", original_url).prepare()
    
    response = Response()
    response.request = original_req
    
    # New request to the same host, different path
    target_url = f"{host}/target"
    auth_header_value = "Basic dXNlcjpwYXNz"
    target_req = Request(
        "GET", 
        target_url, 
        headers={"Authorization": auth_header_value}
    ).prepare()
    
    # Execute
    session.rebuild_auth(target_req, response)
    
    # Verify: Authorization header should persist
    assert "Authorization" in target_req.headers
    assert target_req.headers["Authorization"] == auth_header_value