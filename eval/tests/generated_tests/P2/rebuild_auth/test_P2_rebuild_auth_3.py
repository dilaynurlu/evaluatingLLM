import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_applies_netrc_when_trusted():
    """
    Test that new authentication credentials are recovered from .netrc and applied
    to the request when trust_env is True and credentials exist for the new URL.
    """
    session = Session()
    session.trust_env = True
    # Ensure we don't trip over the stripping logic for this test
    session.should_strip_auth = Mock(return_value=False)

    target_url = "http://authenticated.com/resource"
    netrc_credentials = ("user", "netrc_password")

    # Setup prepared request with no existing auth
    prepared_request = Mock()
    prepared_request.headers = {}
    prepared_request.url = target_url
    # Mock the prepare_auth method which applies credentials
    prepared_request.prepare_auth = Mock()

    response = Mock()
    response.request.url = "http://original.com"

    # Patch get_netrc_auth to return mock credentials
    with patch("requests.sessions.get_netrc_auth", return_value=netrc_credentials) as mock_get_netrc:
        session.rebuild_auth(prepared_request, response)
        
        # Verify get_netrc_auth was called for the new URL
        mock_get_netrc.assert_called_once_with(target_url)
        
        # Verify those credentials were applied to the request
        prepared_request.prepare_auth.assert_called_once_with(netrc_credentials)

'''
Manually marked as assertion correct in the csv because case contains passing assertions, just not recognized by the tool
'''