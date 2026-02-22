import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import SessionRedirectMixin

def test_rebuild_auth_netrc():
    """
    Test that new auth is fetched from netrc if trust_env is True.
    """
    mixin = SessionRedirectMixin()
    mixin.trust_env = True
    mixin.should_strip_auth = MagicMock(return_value=False)
    
    # Mock PreparedRequest
    prep = MagicMock()
    prep.headers = {}
    prep.url = "http://example.com/foo"
    
    # Mock Response
    resp = MagicMock()
    resp.request.url = "http://example.com/bar"
    
    # Patch get_netrc_auth
    with patch("requests.sessions.get_netrc_auth") as mock_gn:
        mock_gn.return_value = ("user", "pass")
        
        mixin.rebuild_auth(prep, resp)
        
        mock_gn.assert_called_with("http://example.com/foo")
        prep.prepare_auth.assert_called_with(("user", "pass"))
