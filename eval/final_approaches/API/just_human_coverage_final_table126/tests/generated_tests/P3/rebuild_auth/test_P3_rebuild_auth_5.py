import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_old_and_adds_new_netrc_auth():
    """
    Test the complex scenario where a redirect crosses domains:
    1. The old 'Authorization' header must be stripped (security).
    2. New credentials from .netrc must be applied for the new domain (functionality).
    """
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        # Credentials for the NEW host
        mock_netrc.return_value = ("new_user", "new_pass")

        session = Session()
        session.trust_env = True

        original_req = PreparedRequest()
        original_req.url = "http://old-host.com/resource"
        
        response = Response()
        response.request = original_req

        # Redirect to new host. 
        # The request object initially contains headers copied from the original request.
        # We explicitly use a different header casing to ensure the stripping logic finds it.
        redirected_req = PreparedRequest()
        redirected_req.url = "http://new-host.com/resource"
        redirected_req.headers = CaseInsensitiveDict({
            "AUTHORIZATION": "Basic b2xkOm9sZA=="  # old:old
        })

        # Execute
        session.rebuild_auth(redirected_req, response)

        # Expected Basic Auth for new creds: base64("new_user:new_pass") -> "bmV3X3VzZXI6bmV3X3Bhc3M="
        expected_auth = "Basic bmV3X3VzZXI6bmV3X3Bhc3M="

        # Verify the final state of the Authorization header
        assert "Authorization" in redirected_req.headers
        
        # It should NOT be the old value
        assert redirected_req.headers["Authorization"] != "Basic b2xkOm9sZA=="
        
        # It SHOULD be the new value derived from netrc
        assert redirected_req.headers["Authorization"] == expected_auth