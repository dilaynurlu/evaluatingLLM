import pytest
from requests import Session, Request, Response

def test_rebuild_auth_strips_authorization_on_cross_host_redirect():
    session = Session()
    # Disable environment trust to isolate the stripping behavior 
    # and ensure netrc doesn't interfere.
    session.trust_env = False

    # 1. Simulate the original request (that got redirected)
    # Origin: http://source.com
    orig_req = Request("GET", "http://source.com/resource")
    orig_prep = orig_req.prepare()
    
    # 2. Simulate the Response that triggered the redirect
    response = Response()
    response.request = orig_prep
    response.status_code = 302
    
    # 3. Simulate the NEW request (to a different host)
    # The session would normally copy headers, so we manually add Authorization
    # to simulate the state before rebuild_auth is called.
    new_req = Request("GET", "http://destination.com/resource", 
                      headers={"Authorization": "Basic old_credentials"})
    new_prep = new_req.prepare()
    
    # Pre-assertion: Authorization header exists
    assert "Authorization" in new_prep.headers
    
    # 4. Call rebuild_auth
    session.rebuild_auth(new_prep, response)
    
    # 5. Assert Authorization header is removed because host changed
    assert "Authorization" not in new_prep.headers