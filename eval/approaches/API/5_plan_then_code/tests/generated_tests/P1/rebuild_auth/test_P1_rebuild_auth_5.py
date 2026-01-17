import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_strips_old_and_applies_new_netrc():
    """
    Test the scenario where old authentication is stripped (due to host change)
    AND new authentication is applied from .netrc in the same operation.
    """
    session = Session()
    session.trust_env = True
    
    # Original Request (Source)
    response = Response()
    response.request = Request(method='GET', url="http://source.com").prepare()
    
    # New Request (Destination) - Different Host, carrying old auth
    new_url = "http://dest.com"
    old_auth = "Basic old_creds"
    headers = {'Authorization': old_auth}
    new_request = Request(method='GET', url=new_url, headers=headers).prepare()
    
    # Credentials to be found in netrc for the new host
    new_user, new_pass = "new_user", "new_pass"
    
    with patch('requests.sessions.get_netrc_auth', return_value=(new_user, new_pass)):
        session.rebuild_auth(new_request, response)
        
    expected_auth = _basic_auth_str(new_user, new_pass)
    
    # Assert old auth is gone and replaced by new auth
    assert new_request.headers['Authorization'] == expected_auth
    assert new_request.headers['Authorization'] != old_auth