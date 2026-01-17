import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_adds_netrc_auth_when_no_auth_header_exists():
    """
    Test that rebuild_auth adds credentials from .netrc if no Authorization header existed previously,
    and trust_env is True.
    """
    session = Session()
    session.trust_env = True

    # Prepare request with NO Authorization header
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://example.com/resource"
    )
    # Ensure no auth header initially
    if "Authorization" in req.headers:
        del req.headers["Authorization"]

    resp = Response()
    resp.request = PreparedRequest()
    resp.request.prepare(method="GET", url="http://example.com/redirected_from")

    # Mock get_netrc_auth to return credentials
    creds = ('netrc_user', 'netrc_pass')
    
    # should_strip_auth won't affect flow since "Authorization" is not in headers,
    # but we can mock it safely or leave it. The key is netrc logic.
    with patch('requests.sessions.get_netrc_auth', return_value=creds):
        session.rebuild_auth(req, resp)
        
        expected_header = _basic_auth_str(*creds)
        assert "Authorization" in req.headers
        assert req.headers["Authorization"] == expected_header