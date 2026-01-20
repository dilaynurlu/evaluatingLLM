
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import patch

def test_rebuild_auth_mock_netrc():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/bar"
    
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")):
        session.rebuild_auth(req, resp)
    
    assert req.headers["Authorization"] is not None
