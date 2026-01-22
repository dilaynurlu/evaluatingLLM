import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_auth_on_https_to_http_downgrade():
    """
    Test that rebuild_auth strips authentication when redirecting from HTTPS
    to HTTP, even on the same host, to prevent sending credentials in cleartext.
    """
    session = Session()
    session.trust_env = False

    # Setup: Original request was Secure (HTTPS)
    original_url = "https://example.com/secure"
    original_req = Request("GET", original_url)
    original_prep = original_req.prepare()

    response = Response()
    response.request = original_prep
    response.url = original_url

    # Setup: Redirect is Insecure (HTTP)
    new_url = "http://example.com/insecure"
    new_req = Request("GET", new_url, headers={"Authorization": "Basic c2VjcmV0OnBhc3N3b3Jk"})
    new_prep = new_req.prepare()

    assert "Authorization" in new_prep.headers

    # Execute
    session.rebuild_auth(new_prep, response)

    # Assert: Authorization stripped due to protocol downgrade
    assert "Authorization" not in new_prep.headers