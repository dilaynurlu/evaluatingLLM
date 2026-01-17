import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response
from requests.auth import HTTPBasicAuth

def test_rebuild_auth_applies_netrc_auth():
    """
    Test that rebuild_auth applies credentials from netrc when trust_env is True.
    """
    session = Session()
    session.trust_env = True
    
    # Original request (no auth necessary for this test setup)
    original_req = Request("GET", "http://example.com").prepare()
    response = Response()
    response.request = original_req
    
    # New request
    new_url = "http://target.com/resource"
    new_req = Request("GET", new_url).prepare()
    
    # Ensure no auth initially
    assert "Authorization" not in new_req.headers
    
    # Mock get_netrc_auth to return credentials for the new host
    # We patch it in requests.sessions because that is where rebuild_auth is defined
    netrc_creds = ("netrc_user", "netrc_pass")
    
    with patch("requests.sessions.get_netrc_auth", return_value=netrc_creds):
        session.rebuild_auth(new_req, response)
    
    # Assert Authorization header is added
    assert "Authorization" in new_req.headers
    
    # Verify the header value matches what we expect for Basic Auth
    expected_header = HTTPBasicAuth(*netrc_creds)(Request()).headers["Authorization"]
    assert new_req.headers["Authorization"] == expected_header