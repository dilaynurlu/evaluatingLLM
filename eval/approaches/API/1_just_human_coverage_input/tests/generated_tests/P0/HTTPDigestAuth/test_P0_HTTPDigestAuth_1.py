import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request

def test_http_digest_auth_registers_hooks():
    """
    Test that initializing HTTPDigestAuth and calling it on a request
    registers the necessary response hooks (handle_401 and handle_redirect).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Create a real Request and prepare it
    request = Request("GET", "http://example.com").prepare()
    
    # Verify hooks are initially empty or default
    assert "response" not in request.hooks or not request.hooks["response"]
    
    # Apply authentication
    auth(request)
    
    # Verify hooks are registered
    assert "response" in request.hooks
    assert auth.handle_401 in request.hooks["response"]
    assert auth.handle_redirect in request.hooks["response"]