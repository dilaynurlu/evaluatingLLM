import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strips_old_and_applies_new_netrc_auth():
    """
    Test the combination: Old auth is stripped due to host change,
    AND new auth is applied from .netrc for the new host.
    """
    session = Session()
    session.trust_env = True
    
    # 1. Original Request (Host A)
    original_req = PreparedRequest()
    original_req.prepare(
        method="GET",
        url="https://host-a.com/data"
    )
    
    response = Response()
    response.request = original_req
    
    # 2. Redirect Request (Host B), carrying old auth initially
    target_url = "https://host-b.com/data"
    redirected_req = PreparedRequest()
    redirected_req.prepare(
        method="GET",
        url=target_url,
        headers={"Authorization": "Basic old_credentials_base64"}
    )
    
    rebuild_auth = Session.rebuild_auth
    
    # 3. Setup Netrc to provide new credentials for Host B
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("new_user", "new_pass")
        
        rebuild_auth(session, redirected_req, response)
    
    # 4. Verify old auth is gone and new auth matches "new_user:new_pass"
    # "new_user:new_pass" -> bmV3X3VzZXI6bmV3X3Bhc3M=
    expected_auth = "Basic bmV3X3VzZXI6bmV3X3Bhc3M="
    
    assert redirected_req.headers["Authorization"] == expected_auth
    # Explicit check to ensure it's not the old one
    assert "old_credentials" not in redirected_req.headers["Authorization"]