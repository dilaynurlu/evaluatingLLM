import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_preserves_header_on_same_host():
    """
    Test that rebuild_auth preserves the Authorization header when redirecting
    to the same host (different path), as credentials are safe to send.
    """
    session = Session()
    session.trust_env = False
    
    # Simulate a prepared request for the NEW location (same host)
    new_url = "http://example.com/new-path"
    new_request = PreparedRequest()
    new_request.url = new_url
    # Header that should be preserved
    auth_header = "Basic c2VjcmV0OnBhc3M="
    new_request.headers = CaseInsensitiveDict({
        "Authorization": auth_header
    })
    
    # Simulate the response from the OLD location
    old_url = "http://example.com/old-path"
    response = Response()
    old_request = PreparedRequest()
    old_request.url = old_url
    response.request = old_request
    
    # Execute the function under test
    session.rebuild_auth(new_request, response)
    
    # Assertions
    assert "Authorization" in new_request.headers
    assert new_request.headers["Authorization"] == auth_header