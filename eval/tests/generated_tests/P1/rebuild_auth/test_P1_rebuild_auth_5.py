import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_old_auth_and_applies_new_netrc_auth():
    """
    Test the scenario where authentication is stripped due to a host change,
    but new authentication is immediately discovered and applied via .netrc.
    """
    session = Session()
    session.trust_env = True

    # Setup: Original request to host A
    original_url = "http://host-a.com/"
    original_req = Request("GET", original_url)
    original_prep = original_req.prepare()

    response = Response()
    response.request = original_prep
    response.url = original_url

    # Setup: Redirect to host B, carrying over host A's credentials initially
    new_url = "http://host-b.com/"
    # Old creds: 'olduser:oldpass' -> b2xkdXNlcjpvbGRwYXNz
    new_req = Request("GET", new_url, headers={"Authorization": "Basic b2xkdXNlcjpvbGRwYXNz"})
    new_prep = new_req.prepare()

    assert new_prep.headers["Authorization"] == "Basic b2xkdXNlcjpvbGRwYXNz"

    # Mock .netrc to provide credentials for host B
    # New creds: 'newuser:newpass' -> bmV3dXNlcjpuZXdwYXNz
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("newuser", "newpass")

        session.rebuild_auth(new_prep, response)

        # Assert: Header should now contain the new credentials
        assert "Authorization" in new_prep.headers
        assert new_prep.headers["Authorization"] == "Basic bmV3dXNlcjpuZXdwYXNz"
        
        # Ensure it was called with the new URL
        mock_netrc.assert_called_with(new_url)