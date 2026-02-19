import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request
import base64

def test_rebuild_auth_applies_netrc_credentials():
    """
    Test that rebuild_auth applies credentials from .netrc if trust_env is True.
    """
    session = Session()
    session.trust_env = True
    
    # Original request
    orig_req = Request('GET', 'http://public.com/')
    response = Response()
    response.request = orig_req.prepare()
    
    # New request to a protected domain
    new_req = PreparedRequest()
    new_req.prepare(method='GET', url='http://protected.com/resource')
    
    # Ensure no auth initially
    assert 'Authorization' not in new_req.headers
    
    # Mock netrc to return credentials for the new URL
    # get_netrc_auth returns a (username, password) tuple
    credentials = ('myuser', 'mypass')
    with patch('requests.sessions.get_netrc_auth', return_value=credentials) as mock_netrc:
        session.rebuild_auth(new_req, response)
        
        # Verify it was called with the new URL
        mock_netrc.assert_called_with('http://protected.com/resource')
    
    # Calculate expected Basic Auth header value
    # "myuser:mypass" -> base64
    expected_b64 = base64.b64encode(b"myuser:mypass").decode('ascii')
    expected_header = f"Basic {expected_b64}"
    
    assert 'Authorization' in new_req.headers
    assert new_req.headers['Authorization'] == expected_header