import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

@pytest.mark.parametrize("original_url, redirect_url", [
    ("http://example.com/resource", "http://malicious.com/sink"),      # Different Host
    ("http://sub1.example.com", "http://sub2.example.com"),            # Different Subdomain
    ("http://example.com:8080", "http://example.com:9090"),            # Different Port
    ("https://secure.com/resource", "http://secure.com/sink"),         # HTTPS to HTTP Downgrade
])
@pytest.mark.parametrize("auth_header_key", ["Authorization", "AUTHORIZATION"])
@pytest.mark.parametrize("auth_value", ["Basic c2VjcmV0OnBhc3N3b3Jk", "Bearer some-token-value"])
def test_rebuild_auth_strips_credentials_on_origin_change(original_url, redirect_url, auth_header_key, auth_value):
    """
    Test that rebuild_auth removes the 'Authorization' header when redirecting
    across boundaries that constitute an origin change:
    1. Host mismatch
    2. Subdomain mismatch
    3. Port mismatch
    4. Protocol downgrade (HTTPS -> HTTP)
    
    Also verifies robustness against header casing and auth schemes (Basic vs Bearer).
    """
    session = Session()
    session.trust_env = False

    # The original request
    original_req = PreparedRequest()
    original_req.url = original_url
    
    response = Response()
    response.request = original_req

    # The new request for the redirect location
    redirected_req = PreparedRequest()
    redirected_req.url = redirect_url
    
    # Pre-populate the redirected request with the sensitive header 
    # (simulating headers being copied before rebuild_auth is called)
    redirected_req.headers = CaseInsensitiveDict({
        auth_header_key: auth_value,
        "Accept": "application/json"
    })

    # Execute
    session.rebuild_auth(redirected_req, response)

    # Verify Authorization is stripped
    assert "Authorization" not in redirected_req.headers
    assert auth_header_key not in redirected_req.headers
    
    # Verify non-sensitive headers remain
    assert redirected_req.headers["Accept"] == "application/json"