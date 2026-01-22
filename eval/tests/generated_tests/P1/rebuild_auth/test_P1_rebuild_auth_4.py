import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_ignores_netrc_when_trust_env_is_false():
    """
    Test that rebuild_auth does NOT apply .netrc credentials if trust_env is False,
    even if credentials exist.
    """
    session = Session()
    session.trust_env = False

    original_url = "http://example.com/"
    original_req = Request("GET", original_url)
    original_prep = original_req.prepare()

    response = Response()
    response.request = original_prep
    response.url = original_url

    new_url = "http://secure.com/resource"
    new_req = Request("GET", new_url)
    new_prep = new_req.prepare()

    # Mock get_netrc_auth to return credentials if called
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("user", "pass")

        session.rebuild_auth(new_prep, response)

        # Assert: Authorization header is NOT present
        assert "Authorization" not in new_prep.headers
        # Additionally, get_netrc_auth should logically not be called or result ignored
        # The implementation uses: get_netrc_auth(url) if self.trust_env else None
        # So we expect it might not be called at all.
        mock_netrc.assert_not_called()