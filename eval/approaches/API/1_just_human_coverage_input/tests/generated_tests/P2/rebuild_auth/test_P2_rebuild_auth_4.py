import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_ignores_netrc_when_env_not_trusted(mock_get_netrc):
    """
    Test that .netrc lookup is skipped (and thus no auth added) when 
    trust_env is False, even if credentials would be available.
    """
    mock_get_netrc.return_value = ("user", "pass")

    session = Session()
    session.trust_env = False  # Disable environment trust
    session.should_strip_auth = Mock(return_value=False)

    prepared_request = Request("GET", "https://example.com/resource").prepare()
    
    response = Response()
    response.request = Request("GET", "https://example.com/old").prepare()

    session.rebuild_auth(prepared_request, response)

    # Assertions
    # Netrc helper should not be called
    mock_get_netrc.assert_not_called()
    # No auth should be added
    assert "Authorization" not in prepared_request.headers