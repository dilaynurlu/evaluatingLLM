import requests
from requests.sessions import Session
from requests.models import Response, Request

def test_rebuild_auth_strips_authorization_on_scheme_downgrade():
    session = Session()
    session.trust_env = False
    
    # Original request was HTTPS
    original_url = "https://secure-site.com/resource"
    original_req = Request("GET", original_url).prepare()
    
    response = Response()
    response.request = original_req
    
    # Redirect target is HTTP (downgrade) on same host
    target_url = "http://secure-site.com/resource"
    auth_val = "Basic c2VjcmV0OnBhc3M="
    target_req = Request(
        "GET", 
        target_url, 
        headers={"Authorization": auth_val}
    ).prepare()
    
    # Requests security policy strips auth on HTTPS -> HTTP downgrade
    session.rebuild_auth(target_req, response)
    
    assert "Authorization" not in target_req.headers