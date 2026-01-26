import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_authorization_header_on_redirect_to_different_host():
    """
    Test that rebuild_auth removes the 'Authorization' header when redirecting
    to a different host, preventing credential leakage.
    """
    session = Session()
    # Disable trust_env to isolate the stripping logic from netrc checks
    session.trust_env = False

    # Setup original request (e.g. http://original.com)
    original_url = "http://original.com/resource"
    original_req = Request("GET", original_url)
    original_prep = original_req.prepare()

    # Setup response associated with original request
    response = Response()
    response.request = original_prep
    response.url = original_url

    # Setup redirected request to a DIFFERENT host
    # We manually add Authorization to simulate it being present before stripping
    new_url = "http://other-host.com/resource"
    new_req = Request("GET", new_url, headers={"Authorization": "Basic c2VjcmV0OnBhc3N3b3Jk"})
    new_prep = new_req.prepare()

    # Verify precondition
    assert "Authorization" in new_prep.headers

    # Execute
    session.rebuild_auth(new_prep, response)

    # Assert: Authorization should be removed
    assert "Authorization" not in new_prep.headers