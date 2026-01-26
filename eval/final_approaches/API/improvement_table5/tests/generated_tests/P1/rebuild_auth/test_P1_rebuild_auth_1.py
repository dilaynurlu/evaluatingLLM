import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_header_on_host_change():
    """
    Test that rebuild_auth removes the Authorization header when redirecting
    to a different host, ensuring credentials are not leaked.
    """
    session = Session()
    # Disable env trust to ensure netrc logic doesn't interfere (returns None)
    session.trust_env = False
    
    # Simulate a prepared request for the NEW location (target of redirect)
    new_url = "http://new-host.com/resource"
    new_request = PreparedRequest()
    new_request.url = new_url
    new_request.headers = CaseInsensitiveDict({
        "Authorization": "Basic c2VjcmV0OnBhc3M="  # 'secret:pass'
    })
    
    # Simulate the response from the OLD location (source of redirect)
    old_url = "http://old-host.com/resource"
    response = Response()
    old_request = PreparedRequest()
    old_request.url = old_url
    response.request = old_request
    
    # Execute the function under test
    session.rebuild_auth(new_request, response)
    
    # Assertions
    assert "Authorization" not in new_request.headers, "Authorization header should be stripped on host change"