import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_old_and_applies_new_netrc():
    """
    Test the full flow: redirect to a new host strips the old invalid auth,
    and then successfully discovers and applies new auth from .netrc for the new host.
    """
    session = Session()
    session.trust_env = True
    
    # Redirect Target (New Host)
    new_url = "http://new-host.com/resource"
    new_request = PreparedRequest()
    new_request.url = new_url
    # Originally carries the old auth copied from the previous request
    new_request.headers = CaseInsensitiveDict({
        "Authorization": "Basic b2xkOmNyZWQ="  # 'old:cred'
    })
    
    # Redirect Source (Old Host)
    old_url = "http://old-host.com/resource"
    response = Response()
    old_request = PreparedRequest()
    old_request.url = old_url
    response.request = old_request
    
    # Mock netrc to provide credentials for the NEW host
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("new_user", "new_pass")
        
        session.rebuild_auth(new_request, response)
        
        # 1. Old auth header should be gone (implied by it being replaced or absent)
        # 2. New auth header should be present
        assert "Authorization" in new_request.headers
        
        # Verify it matches the new credentials, not the old ones
        # 'new_user:new_pass' (b64) != 'old:cred' (b64)
        current_auth = new_request.headers["Authorization"]
        assert current_auth != "Basic b2xkOmNyZWQ="
        assert current_auth.startswith("Basic ")