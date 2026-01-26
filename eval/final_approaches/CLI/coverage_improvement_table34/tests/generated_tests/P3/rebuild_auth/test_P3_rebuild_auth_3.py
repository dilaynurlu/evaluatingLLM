import pytest
import os
from requests.sessions import SessionRedirectMixin
from requests.models import PreparedRequest, Response
from unittest.mock import Mock, patch

def test_rebuild_auth_netrc():
    mixin = SessionRedirectMixin()
    mixin.trust_env = True
    
    req = PreparedRequest()
    req.url = "http://example.com/page1"
    req.headers = {}
    
    resp = Mock(spec=Response)
    resp.request = Mock(spec=PreparedRequest)
    resp.request.url = "http://other.com/login"
    
    with patch("requests.sessions.get_netrc_auth") as mock_gn:
        mock_gn.return_value = ("user", "pass")
        mixin.rebuild_auth(req, resp)
    
    assert "Authorization" in req.headers
    assert req.headers["Authorization"].startswith("Basic ")
