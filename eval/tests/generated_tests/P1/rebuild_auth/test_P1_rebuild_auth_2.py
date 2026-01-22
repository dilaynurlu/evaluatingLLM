import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_preserves_authorization_header_on_redirect_to_same_host():
    """
    Test that rebuild_auth preserves the 'Authorization' header when redirecting
    to the same host (same domain and port).
    """
    session = Session()
    session.trust_env = False

    # Setup original request
    original_url = "http://original.com/resource"
    original_req = Request("GET", original_url)
    original_prep = original_req.prepare()

    response = Response()
    response.request = original_prep
    response.url = original_url

    # Setup redirected request to the SAME host but different path
    new_url = "http://original.com/other-path"
    new_req = Request("GET", new_url, headers={"Authorization": "Basic c2VjcmV0OnBhc3N3b3Jk"})
    new_prep = new_req.prepare()

    # Verify precondition
    assert "Authorization" in new_prep.headers
    original_auth_value = new_prep.headers["Authorization"]

    # Execute
    session.rebuild_auth(new_prep, response)

    # Assert: Authorization should remain unchanged
    assert "Authorization" in new_prep.headers
    assert new_prep.headers["Authorization"] == original_auth_value