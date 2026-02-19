import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_retains_authorization_on_same_host():
    """
    Test that rebuild_auth preserves the 'Authorization' header when redirecting
    to a URL on the same host.
    """
    session = Session()
    
    # 1. Setup original request
    original_req = PreparedRequest()
    original_req.url = "https://example.com/page1"
    
    response = Response()
    response.request = original_req
    
    # 2. Setup new request (same host, different path)
    new_req = PreparedRequest()
    new_req.url = "https://example.com/page2"
    new_req.headers = CaseInsensitiveDict({
        "Authorization": "Basic c2VjcmV0OnBhc3N3b3Jk"
    })
    
    # 3. Call target function
    # Same host -> should_strip_auth should return False
    session.rebuild_auth(new_req, response)
    
    # 4. Verification
    assert "Authorization" in new_req.headers
    assert new_req.headers["Authorization"] == "Basic c2VjcmV0OnBhc3N3b3Jk"