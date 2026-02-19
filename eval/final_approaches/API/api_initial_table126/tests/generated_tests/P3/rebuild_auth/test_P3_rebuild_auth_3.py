import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_adds_netrc_auth_when_trusted():
    """
    Test that rebuild_auth adds credentials from .netrc when trust_env is True.
    Verifies that the lookup uses the correct redirected URL.
    """
    # Patch the get_netrc_auth function used internally by rebuild_auth
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        # Simulate finding credentials for the target host
        mock_netrc.return_value = ("netrc_user", "netrc_pass")

        session = Session()
        session.trust_env = True

        original_req = PreparedRequest()
        original_req.url = "http://start.com"
        
        response = Response()
        response.request = original_req

        # Redirect target matches the mocked netrc credentials
        # Using a URL with a path to ensure get_netrc_auth receives the full context if needed
        target_url = "http://target-with-netrc.com/resource"
        redirected_req = PreparedRequest()
        redirected_req.url = target_url
        redirected_req.headers = CaseInsensitiveDict({})

        # Execute
        session.rebuild_auth(redirected_req, response)

        # Expected Basic Auth: base64("netrc_user:netrc_pass") -> "bmV0cmNfdXNlcjpuZXRyY19wYXNz"
        expected_auth = "Basic bmV0cmNfdXNlcjpuZXRyY19wYXNz"

        # Verify new auth added
        assert "Authorization" in redirected_req.headers
        assert redirected_req.headers["Authorization"] == expected_auth
        
        # Verify get_netrc_auth was called with the new URL to resolve credentials correctly
        mock_netrc.assert_called_with(target_url)