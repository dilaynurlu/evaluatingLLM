import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Test that .netrc credentials are NOT looked up or applied when trust_env is False,
    even if credentials would otherwise be available.
    """
    session = Session()
    session.trust_env = False  # Disable environment trust
    session.should_strip_auth = Mock(return_value=False)

    prepared_request = Mock()
    prepared_request.headers = {}
    prepared_request.url = "http://internal.com"
    prepared_request.prepare_auth = Mock()

    response = Mock()
    response.request.url = "http://other.com"

    # Patch get_netrc_auth to return credentials if it were called
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")) as mock_get_netrc:
        session.rebuild_auth(prepared_request, response)
        
        # Verify get_netrc_auth was NOT called (short-circuit logic)
        assert not mock_get_netrc.called
        
        # Verify prepare_auth was NOT called
        prepared_request.prepare_auth.assert_not_called()