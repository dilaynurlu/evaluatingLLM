import pytest
from requests import Session, PreparedRequest, Response

@pytest.mark.parametrize("original_url, new_url, should_strip", [
    # Different Host -> Strip
    ("http://old-host.com/resource", "http://new-host.com/resource", True),
    # Same Host -> Keep
    ("http://example.com/old", "http://example.com/new", False),
    # Different Port -> Strip
    ("http://example.com:80/resource", "http://example.com:8080/resource", True),
    # Protocol Downgrade (HTTPS -> HTTP) -> Strip
    ("https://example.com/resource", "http://example.com/resource", True),
    # Protocol Upgrade (HTTP -> HTTPS) -> Keep
    ("http://example.com/resource", "https://example.com/resource", False),
    # Subdomain Change -> Strip
    ("http://a.example.com/resource", "http://b.example.com/resource", True),
    # Parent to Subdomain -> Strip
    ("http://example.com/resource", "http://sub.example.com/resource", True),
])
def test_rebuild_auth_stripping_behavior(original_url, new_url, should_strip):
    """
    Test that rebuild_auth correctly strips or preserves the Authorization header
    based on changes in host, port, and protocol scheme.
    """
    session = Session()
    # Disable environment trust to isolate the stripping logic from .netrc checks
    session.trust_env = False

    # Prepare request for the NEW URL with an existing Authorization header
    p_req = PreparedRequest()
    
    # Use lowercase header key for one case to verify case-insensitive handling
    # Requests CaseInsensitiveDict should handle this normalization.
    headers = {"Authorization": "Bearer secret_token"}
    if should_strip:
        # Vary casing to ensure logic is robust against different input casings
        headers = {"authorization": "Bearer secret_token"}
        
    p_req.prepare(method="GET", url=new_url, headers=headers)

    # Create response representing the redirect source (ORIGINAL URL)
    original_req = PreparedRequest()
    original_req.url = original_url
    
    response = Response()
    response.request = original_req

    # Execute
    session.rebuild_auth(p_req, response)

    # Assertions
    if should_strip:
        assert "Authorization" not in p_req.headers, \
            f"Auth should be stripped when redirecting from {original_url} to {new_url}"
    else:
        assert "Authorization" in p_req.headers, \
            f"Auth should be preserved when redirecting from {original_url} to {new_url}"
        assert p_req.headers["Authorization"] == "Bearer secret_token"