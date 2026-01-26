import pytest
from requests.sessions import SessionRedirectMixin
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_rebuild_auth_diff_host():
    mixin = SessionRedirectMixin()
    mixin.trust_env = False
    
    req = PreparedRequest()
    req.url = "http://evil.com/page1"
    req.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    
    resp = Mock(spec=Response)
    resp.request = Mock(spec=PreparedRequest)
    resp.request.url = "http://example.com/login"
    
    mixin.rebuild_auth(req, resp)
    
    assert "Authorization" not in req.headers
