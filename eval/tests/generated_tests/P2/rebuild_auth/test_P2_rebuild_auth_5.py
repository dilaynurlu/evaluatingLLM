import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_replaces_stripped_auth_with_netrc():
    """
    Test the full flow where existing Authorization is stripped (due to redirect rules)
    AND new Authorization is applied from .netrc for the new host.
    """
    session = Session()
    session.trust_env = True
    
    # Simulate condition to strip auth (e.g., cross-domain redirect)
    session.should_strip_auth = Mock(return_value=True)

    new_url = "http://new-domain.com/resource"
    netrc_creds = ("new_user", "new_pass")

    # Request has old credentials
    prepared_request = Mock()
    prepared_request.headers = {"Authorization": "Basic old_creds"}
    prepared_request.url = new_url
    prepared_request.prepare_auth = Mock()

    response = Mock()
    response.request.url = "http://old-domain.com/resource"

    with patch("requests.sessions.get_netrc_auth", return_value=netrc_creds):
        session.rebuild_auth(prepared_request, response)

    # 1. Verify old Authorization header was deleted
    assert "Authorization" not in prepared_request.headers

    # 2. Verify new credentials were applied
    prepared_request.prepare_auth.assert_called_once_with(netrc_creds)