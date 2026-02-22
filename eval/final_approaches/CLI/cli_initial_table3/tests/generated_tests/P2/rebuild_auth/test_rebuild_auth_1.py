import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin

def test_rebuild_auth_strip_auth():
    """
    Test that Authorization header is removed if should_strip_auth returns True.
    """
    mixin = SessionRedirectMixin()
    mixin.trust_env = False
    
    # Mock should_strip_auth
    mixin.should_strip_auth = MagicMock(return_value=True)
    
    # Mock PreparedRequest
    prep = MagicMock()
    prep.headers = {"Authorization": "Basic ..."}
    prep.url = "http://new.example.com/"
    
    # Mock Response
    resp = MagicMock()
    resp.request.url = "http://old.example.com/"
    
    mixin.rebuild_auth(prep, resp)
    
    assert "Authorization" not in prep.headers
    mixin.should_strip_auth.assert_called_with("http://old.example.com/", "http://new.example.com/")
