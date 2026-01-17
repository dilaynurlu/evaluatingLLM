import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_applies_netrc_auth_when_trusted():
    """
    Test that rebuild_auth applies credentials from .netrc when trusted.
    
    Refinements based on critique:
    - Uses an IP address instead of a hostname to ensure logic handles IP literals.
    """
    session = Session()
    
    # Original request context
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="http://192.168.1.50/source")
    
    response = Response()
    response.request = original_req
    
    # New request to same IP (or different, logic for netrc applies if creds found)
    # Using an IP address for the target
    target_ip = "192.168.1.100"
    new_req = PreparedRequest()
    new_req.prepare(method="GET", url=f"http://{target_ip}/target")
    
    user, pwd = "ip_user", "ip_pass"
    
    # Mock get_netrc_auth. It is typically called with the hostname/IP from the URL.
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = (user, pwd)
        
        session.rebuild_auth(new_req, response)
        
        # Verify the mock was called with the correct IP
        args, _ = mock_netrc.call_args
        # The first arg to get_netrc_auth is the host
        assert target_ip in args[0]
    
    # Assertion: Authorization header should be added using netrc credentials
    expected_auth = _basic_auth_str(user, pwd)
    assert "Authorization" in new_req.headers
    assert new_req.headers["Authorization"] == expected_auth