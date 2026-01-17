import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_preserves_header_on_same_host_redirect():
    """
    Test that rebuild_auth preserves the 'Authorization' header when redirecting
    to the same host, correctly handling URI normalization.
    
    Refinements based on critique:
    - Verifies that URL casing differences (URI normalization) do not trigger stripping.
    """
    session = Session()
    
    # Setup the original request (lowercase host)
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="http://example.com/source")
    
    response = Response()
    response.request = original_req
    
    # Setup new request with UPPERCASE host (should be treated as same origin)
    auth_header_value = "Basic c2VjcmV0OnBhc3M="
    new_req = PreparedRequest()
    new_req.prepare(
        method="GET", 
        url="http://EXAMPLE.COM/target", 
        headers={"Authorization": auth_header_value}
    )
    
    # Action
    session.rebuild_auth(new_req, response)
    
    # Assertion: Authorization header should remain because example.com == EXAMPLE.COM
    assert "Authorization" in new_req.headers
    assert new_req.headers["Authorization"] == auth_header_value