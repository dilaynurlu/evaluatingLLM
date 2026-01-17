import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strips_header_on_cross_domain_redirect():
    """
    Test that rebuild_auth removes the 'Authorization' header when redirecting
    to a different host.
    
    Refinements based on critique:
    - Verifies handling of non-Basic auth schemes (Bearer).
    - Verifies case-insensitivity of the Authorization header key.
    """
    session = Session()
    
    # Setup the original request
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="http://example.com/source")
    
    response = Response()
    response.request = original_req
    
    # Setup the new request for the redirect target (different host)
    new_req = PreparedRequest()
    
    # Initialize with headers using mixed-case key and Bearer scheme
    # Note: PreparedRequest.prepare normalizes headers, but we want to ensure
    # the stripping logic works regardless of how the header was introduced.
    new_req.prepare(
        method="GET", 
        url="http://other-domain.com/target", 
        headers={"aUtHoRiZaTiOn": "Bearer sensitive-token-123"}
    )
    
    # Pre-condition check (accessing case-insensitively)
    assert "Authorization" in new_req.headers
    assert new_req.headers["Authorization"] == "Bearer sensitive-token-123"
    
    # Action: Rebuild auth
    session.rebuild_auth(new_req, response)
    
    # Assertion: Header should be removed due to host mismatch
    # Checking various casing possibilities to ensure complete removal
    assert "Authorization" not in new_req.headers
    assert "authorization" not in new_req.headers
    assert "AuThOrIzAtIoN" not in new_req.headers