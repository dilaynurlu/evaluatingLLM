import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_strips_credentials_on_unsafe_transitions():
    """
    Refined test based on critique:
    Verifies that Authorization headers are stripped during unsafe redirect transitions.
    Coverage includes:
    1. Protocol downgrade (HTTPS -> HTTP) on same host.
    2. Port change on same host.
    3. Host change (different domain).
    4. Subdomain change.
    
    Also verifies that the stripping logic is case-insensitive regarding the header key.
    """
    session = Session()
    # Disable trust_env to rely solely on the stripping logic, avoiding netrc interference
    session.trust_env = False
    
    # Dynamic credential generation
    auth_val = _basic_auth_str('sensitive', 'data')
    
    # List of (original_url, redirect_url) tuples
    scenarios = [
        # Protocol Downgrade (Critical Security Check)
        ("https://example.com/resource", "http://example.com/resource"),
        
        # Port Change (Cross-port is considered cross-origin)
        ("http://example.com:8080/resource", "http://example.com:9000/resource"),
        
        # Domain Change
        ("http://example.com/resource", "http://malicious.com/resource"),
        
        # Subdomain Change
        ("http://secure.example.com/resource", "http://public.example.com/resource"),
    ]
    
    for orig_url, new_url in scenarios:
        # Mock the original response
        resp = Response()
        resp.request = PreparedRequest()
        resp.request.url = orig_url
        
        # Mock the new prepared request carrying sensitive headers (as if copied from original)
        prep = PreparedRequest()
        prep.url = new_url
        
        # Use mixed-case header key to verify case-insensitive removal
        prep.headers = requests.structures.CaseInsensitiveDict({
            "AuThOrIzAtIoN": auth_val,
            "X-Safe-Header": "keep-me"
        })
        
        # Execute
        session.rebuild_auth(prep, resp)
        
        # Assert
        # The sensitive Authorization header must be removed
        assert "Authorization" not in prep.headers, f"Failed to strip credentials for {orig_url} -> {new_url}"
        # Other headers should remain
        assert prep.headers.get("X-Safe-Header") == "keep-me"