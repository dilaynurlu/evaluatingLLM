
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_no_initial_auth():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://other.com/bar"
    
    # Mock get_netrc_auth to return None to isolate test
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        session.rebuild_auth(req, resp)
    
    assert "Authorization" not in req.headers
from unittest.mock import patch
