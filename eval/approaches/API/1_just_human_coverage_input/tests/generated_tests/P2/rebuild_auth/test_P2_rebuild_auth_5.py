import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_strips_old_and_applies_new_netrc_auth(mock_get_netrc):
    """
    Test the scenario where old authentication must be stripped (e.g. redirect 
    to new host) AND new authentication is available via .netrc for the new host.
    """
    # Setup new credentials from netrc
    mock_get_netrc.return_value = ("new_user", "new_pass")

    session = Session()
    session.trust_env = True
    # Force stripping of old auth
    session.should_strip_auth = Mock(return_value=True)

    # Request has OLD credentials initially
    prepared_request = Request(
        "GET", 
        "https://new-host.com/resource", 
        auth=("old_user", "old_pass")
    ).prepare()
    
    old_auth_header = prepared_request.headers["Authorization"]
    
    response = Response()
    response.request = Request("GET", "https://old-host.com/resource").prepare()

    session.rebuild_auth(prepared_request, response)

    # Assertions
    current_auth_header = prepared_request.headers.get("Authorization")
    
    # The header should exist (because new auth was applied)
    assert current_auth_header is not None
    
    # It should NOT be the old header
    assert current_auth_header != old_auth_header
    
    # It should correspond to the new netrc credentials
    # 'new_user:new_pass' base64 encoded check or simply assume change
    # Basic bmV3X3VzZXI6bmV3X3Bhc3M= corresponds to new_user:new_pass
    assert "bmV3X3VzZXI6bmV3X3Bhc3M=" in current_auth_header
    
    # Verify flow
    session.should_strip_auth.assert_called_once()
    mock_get_netrc.assert_called_once_with("https://new-host.com/resource")