import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str
from unittest.mock import patch

def test_rebuild_auth_strips_old_and_applies_netrc():
    """
    Refined test: Verifies the interaction between header stripping and netrc application.
    
    Scenario:
    Redirecting from Host A to Host B.
    - Host A had credentials (which are copied to Host B's request initially).
    - Host B has *different* credentials in .netrc.
    
    Goal:
    Ensure the old credentials from Host A are stripped, and replaced by Host B's netrc credentials.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Simulate netrc returning NEW credentials for the new URL
        mock_get_netrc.return_value = ("new_user", "new_pass")

        session = Session()
        session.trust_env = True

        # Original request (Host A)
        resp = Response()
        resp.request = PreparedRequest()
        resp.request.url = "http://host-a.com/resource"

        # New request (Host B)
        # Initially contains Host A's credentials (simulating header copy behavior before rebuild)
        prep = PreparedRequest()
        prep.url = "http://host-b.com/resource"
        old_auth = _basic_auth_str("old_user", "old_pass")
        prep.headers = requests.structures.CaseInsensitiveDict({
            "Authorization": old_auth
        })

        # Execute
        session.rebuild_auth(prep, resp)

        # Assert
        # 1. Verify Netrc was queried for the NEW host
        mock_get_netrc.assert_called_with("http://host-b.com/resource")
        
        # 2. Verify headers are updated correctly
        assert "Authorization" in prep.headers
        
        expected_new_auth = _basic_auth_str("new_user", "new_pass")
        # Should NOT equal the old auth
        assert prep.headers["Authorization"] != old_auth
        # Should equal the new netrc auth
        assert prep.headers["Authorization"] == expected_new_auth