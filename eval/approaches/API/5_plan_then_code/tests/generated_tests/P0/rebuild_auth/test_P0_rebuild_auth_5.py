import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_ignores_netrc_when_trust_env_is_false():
    """
    Test that rebuild_auth does NOT call get_netrc_auth or modify headers if trust_env is False,
    even if credentials might be available.
    """
    session = Session()
    session.trust_env = False

    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://example.com/resource"
    )
    # Ensure no auth header
    req.headers.pop("Authorization", None)

    resp = Response()
    resp.request = PreparedRequest()
    resp.request.prepare(method="GET", url="http://example.com/redirected_from")

    # Patch get_netrc_auth to fail if called, ensuring it is NOT called
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        session.rebuild_auth(req, resp)
        
        mock_netrc.assert_not_called()
        assert "Authorization" not in req.headers