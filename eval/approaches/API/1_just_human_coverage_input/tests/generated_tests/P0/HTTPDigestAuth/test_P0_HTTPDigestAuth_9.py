import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_http_digest_auth_ignore_success_status():
    """
    Test that handle_401 returns the response unmodified if the status code is not 4xx.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.hooks = {"response": []}
    auth(req)
    
    resp = Mock(spec=Response)
    resp.status_code = 200  # Success
    resp.request = req
    resp.headers = {}
    resp.connection = Mock()
    
    result = auth.handle_401(resp)
    
    assert result == resp
    assert not resp.connection.send.called