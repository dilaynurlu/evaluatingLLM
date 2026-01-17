import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str
from unittest.mock import patch

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Refined test: Verifies that netrc is ignored when trust_env is False.
    
    Also verifies that if a redirect occurs to a new host, existing credentials 
    are stripped and *not* replaced by netrc (resulting in no auth).
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Simulate netrc having credentials available
        mock_get_netrc.return_value = ("user", "pass")

        session = Session()
        session.trust_env = False  # Feature under test

        # Original request (Host A)
        resp = Response()
        resp.request = PreparedRequest()
        resp.request.url = "http://host-a.com"

        # New request (Host B)
        # Pre-populate with old auth to ensure it gets stripped
        prep = PreparedRequest()
        prep.url = "http://host-b.com"
        prep.headers = requests.structures.CaseInsensitiveDict({
            "Authorization": _basic_auth_str("old", "cred")
        })

        # Execute
        session.rebuild_auth(prep, resp)

        # Assert
        # 1. Authorization should be gone (stripped due to host change)
        assert "Authorization" not in prep.headers
        
        # 2. Netrc should NOT have been queried (optimization check)
        mock_get_netrc.assert_not_called()