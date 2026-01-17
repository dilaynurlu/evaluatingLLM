import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import patch

def test_rebuild_auth_no_change_if_netrc_returns_none():
    """
    Refined test: Verifies that no changes are made if netrc returns None (no credentials found),
    assuming trust_env is True and no previous credentials existed to strip.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Simulate no credentials found
        mock_get_netrc.return_value = None

        session = Session()
        session.trust_env = True

        resp = Response()
        resp.request = PreparedRequest()
        resp.request.url = "http://old-site.com"

        prep = PreparedRequest()
        prep.url = "http://new-site.com"
        prep.headers = requests.structures.CaseInsensitiveDict()

        # Execute
        session.rebuild_auth(prep, resp)

        # Assert
        assert "Authorization" not in prep.headers
        mock_get_netrc.assert_called_with("http://new-site.com")