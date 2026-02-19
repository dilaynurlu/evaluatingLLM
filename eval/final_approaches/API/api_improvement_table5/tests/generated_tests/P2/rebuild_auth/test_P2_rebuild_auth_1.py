import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_authorization_on_host_change():
    """
    Test that rebuild_auth removes the 'Authorization' header when redirecting
    to a different host, preventing credential leakage.
    """
    session = Session()
    
    # 1. Setup the original request (context for the redirect)
    # The URL here represents where we are coming from.
    original_req = PreparedRequest()
    original_req.url = "https://example.com/sensitive-data"
    
    response = Response()
    response.request = original_req
    
    # 2. Setup the new prepared request (destination of redirect)
    # Assume the Authorization header was copied over during the initial prepare phase
    # or persisted from the session.
    new_req = PreparedRequest()
    new_req.url = "https://malicious-site.com/capture"
    new_req.headers = CaseInsensitiveDict({
        "Authorization": "Basic c2VjcmV0OnBhc3N3b3Jk"  # "secret:password"
    })
    
    # 3. Call the target function
    # Because the host changes (example.com -> malicious-site.com), 
    # Session.should_strip_auth should return True.
    session.rebuild_auth(new_req, response)
    
    # 4. Verification
    assert "Authorization" not in new_req.headers