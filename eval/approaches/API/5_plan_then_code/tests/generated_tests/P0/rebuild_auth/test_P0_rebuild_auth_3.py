import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_applies_netrc_after_stripping_old_auth():
    """
    Test that rebuild_auth applies new credentials from .netrc after stripping old authentication,
    if trust_env is True.
    """
    session = Session()
    session.trust_env = True

    # Prepare request with old credentials that should be stripped
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://new-host.com/resource",
        headers={"Authorization": "Basic old_credentials"}
    )

    resp = Response()
    resp.request = PreparedRequest()
    resp.request.prepare(method="GET", url="http://old-host.com/resource")

    # Mock should_strip_auth to True so the old header is removed
    # Mock get_netrc_auth to return new credentials
    new_creds = ('new_user', 'new_pass')
    
    with patch.object(session, 'should_strip_auth', return_value=True):
        with patch('requests.sessions.get_netrc_auth', return_value=new_creds) as mock_get_netrc:
            session.rebuild_auth(req, resp)
            
            mock_get_netrc.assert_called_with(req.url)
            
            # The old header should be gone, replaced by the new one
            # _basic_auth_str helper constructs the expected Basic Auth header value
            expected_header = _basic_auth_str(*new_creds)
            
            assert "Authorization" in req.headers
            assert req.headers["Authorization"] == expected_header
            assert req.headers["Authorization"] != "Basic old_credentials"