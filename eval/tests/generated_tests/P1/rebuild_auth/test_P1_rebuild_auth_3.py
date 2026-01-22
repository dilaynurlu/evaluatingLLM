import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_applies_netrc_auth_when_trust_env_is_true():
    """
    Test that rebuild_auth retrieves credentials from .netrc and applies them
    to the prepared request when trust_env is True.
    """
    session = Session()
    session.trust_env = True

    # Setup original request
    original_url = "http://example.com/"
    original_req = Request("GET", original_url)
    original_prep = original_req.prepare()

    response = Response()
    response.request = original_prep
    response.url = original_url

    # Setup redirected request with NO existing auth
    new_url = "http://secure.com/resource"
    new_req = Request("GET", new_url)
    new_prep = new_req.prepare()

    assert "Authorization" not in new_prep.headers

    # Mock get_netrc_auth to return specific credentials for the new URL
    # ('myuser', 'mypass') -> Basic bXl1c2VyOm15cGFzcw==
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("myuser", "mypass")

        session.rebuild_auth(new_prep, response)

        # Assert: get_netrc_auth called and header applied
        mock_netrc.assert_called_with(new_url)
        assert "Authorization" in new_prep.headers
        assert new_prep.headers["Authorization"] == "Basic bXl1c2VyOm15cGFzcw=="