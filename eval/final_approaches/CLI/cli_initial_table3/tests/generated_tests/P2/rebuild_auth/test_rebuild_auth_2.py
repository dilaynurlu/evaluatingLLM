import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin

def test_rebuild_auth_keep_auth():
    """
    Test that Authorization header is kept if should_strip_auth returns False.
    """
    mixin = SessionRedirectMixin()
    mixin.trust_env = False
    
    # Mock should_strip_auth
    mixin.should_strip_auth = MagicMock(return_value=False)
    
    # Mock PreparedRequest
    prep = MagicMock()
    prep.headers = {"Authorization": "Basic ..."}
    prep.url = "http://example.com/new"
    
    # Mock Response
    resp = MagicMock()
    resp.request.url = "http://example.com/old"
    
    mixin.rebuild_auth(prep, resp)
    
    assert "Authorization" in prep.headers
    assert prep.headers["Authorization"] == "Basic ..."
