import pytest
from requests import Session, Request, Response

def test_rebuild_auth_preserves_authorization_on_same_host_redirect():
    session = Session()
    session.trust_env = False

    # Origin: http://example.com/page1
    orig_req = Request("GET", "http://example.com/page1")
    orig_prep = orig_req.prepare()
    
    response = Response()
    response.request = orig_prep
    
    # Redirect Target: http://example.com/page2 (Same Host)
    new_req = Request("GET", "http://example.com/page2", 
                      headers={"Authorization": "Basic keep_me"})
    new_prep = new_req.prepare()
    
    assert "Authorization" in new_prep.headers
    
    session.rebuild_auth(new_prep, response)
    
    # Assert header is still there because host did not change
    assert "Authorization" in new_prep.headers
    assert new_prep.headers["Authorization"] == "Basic keep_me"