import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import SessionRedirectMixin

def test_rebuild_auth_no_netrc_untrusted():
    """
    Test that netrc is ignored if trust_env is False.
    """
    mixin = SessionRedirectMixin()
    mixin.trust_env = False
    
    # Mock PreparedRequest
    prep = MagicMock()
    prep.headers = {}
    prep.url = "http://example.com/foo"
    
    # Mock Response
    resp = MagicMock()
    resp.request.url = "http://example.com/bar"
    
    # Patch get_netrc_auth to ensure it's not called or ignored
    with patch("requests.sessions.get_netrc_auth") as mock_gn:
        mixin.rebuild_auth(prep, resp)
        
        # It might be called but ignored, or not called. 
        # Code: new_auth = get_netrc_auth(url) if self.trust_env else None
        assert not mock_gn.called
