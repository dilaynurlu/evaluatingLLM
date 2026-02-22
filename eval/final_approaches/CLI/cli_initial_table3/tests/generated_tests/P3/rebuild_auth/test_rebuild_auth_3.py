import pytest
from requests.sessions import Session
from requests.models import Response, Request
from unittest.mock import patch

def test_rebuild_auth_3():
    s = Session()
    s.trust_env = True
    
    # Prep request without auth
    req = Request("GET", "http://example.com/foo")
    original_prep = s.prepare_request(req)
    
    # Mock response
    resp = Response()
    resp.request = original_prep
    resp.url = "http://example.com/foo"
    
    # New request (redirected)
    new_prep = original_prep.copy()
    new_prep.url = "http://other.com/bar"
    
    # Mock get_netrc_auth
    with patch('requests.sessions.get_netrc_auth', return_value=("netrc_user", "netrc_pass")):
        s.rebuild_auth(new_prep, resp)
    
    assert "Authorization" in new_prep.headers
    # "netrc_user":"netrc_pass" -> bmV0cmNfdXNlcjpuZXRyY19wYXNz
    assert new_prep.headers["Authorization"] == "Basic bmV0cmNfdXNlcjpuZXRyY19wYXNz"
