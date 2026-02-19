import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_applies_netrc_auth_when_trusted():
    """
    Test that rebuild_auth queries .netrc and applies new credentials 
    if trust_env is True and credentials exist for the new URL.
    """
    session = Session()
    session.trust_env = True
    
    target_url = "http://api.example.com/data"
    
    new_request = PreparedRequest()
    new_request.url = target_url
    # Start with no auth headers
    new_request.headers = CaseInsensitiveDict({})
    
    # Response context (same host to simplify, focus is on netrc application)
    response = Response()
    old_request = PreparedRequest()
    old_request.url = "http://api.example.com/login"
    response.request = old_request
    
    # Mock get_netrc_auth to return valid credentials
    # We patch strictly where it is used in the target module requests.sessions
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        
        session.rebuild_auth(new_request, response)
        
        # Verify netrc was checked for the correct URL
        mock_netrc.assert_called_with(target_url)
        
        # Verify Auth header was applied
        # ('netrc_user', 'netrc_pass') -> Basic Auth
        assert "Authorization" in new_request.headers
        # We assume standard requests behavior for tuple auth (Basic)
        assert new_request.headers["Authorization"].startswith("Basic ")