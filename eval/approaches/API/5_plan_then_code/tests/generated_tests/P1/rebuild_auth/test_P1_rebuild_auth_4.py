import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_skips_netrc_if_env_untrusted():
    """
    Test that .netrc lookup is skipped entirely if trust_env is False,
    ensuring no new auth is applied even if available in environment.
    """
    session = Session()
    session.trust_env = False
    
    response = Response()
    response.request = Request(method='GET', url="http://example.com").prepare()
    
    new_url = "http://internal.api/resource"
    new_request = Request(method='GET', url=new_url).prepare()
    
    # Mock get_netrc_auth to ensure it is NOT called
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        session.rebuild_auth(new_request, response)
        mock_netrc.assert_not_called()
    
    assert 'Authorization' not in new_request.headers