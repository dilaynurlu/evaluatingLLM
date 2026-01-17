
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import patch

def test_rebuild_auth_trust_env_false():
    session = Session()
    session.trust_env = False
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.headers = {}
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://example.com/bar"
    
    # Even if netrc would return something
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")):
        session.rebuild_auth(req, resp)
    
    assert "Authorization" not in req.headers
