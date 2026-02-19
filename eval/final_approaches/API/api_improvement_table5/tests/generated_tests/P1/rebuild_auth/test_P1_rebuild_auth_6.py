import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_on_scheme_downgrade():
    """
    Test that rebuild_auth strips authentication when redirecting from HTTPS to HTTP,
    even on the same host, to prevent sending credentials over cleartext.
    """
    session = Session()
    session.trust_env = False
    
    # New Request: HTTP (insecure)
    new_url = "http://secure.com/resource"
    new_request = PreparedRequest()
    new_request.url = new_url
    new_request.headers = CaseInsensitiveDict({
        "Authorization": "Basic c2VjcmV0OnBhc3M="
    })
    
    # Old Request: HTTPS (secure)
    old_url = "https://secure.com/resource"
    response = Response()
    old_request = PreparedRequest()
    old_request.url = old_url
    response.request = old_request
    
    session.rebuild_auth(new_request, response)
    
    assert "Authorization" not in new_request.headers