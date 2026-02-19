import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

@pytest.mark.parametrize("header_case", ["Authorization", "AUTHORIZATION"])
def test_rebuild_auth_preserves_auth_on_same_origin(header_case):
    """
    Test that rebuild_auth keeps the 'Authorization' header when redirecting
    to the exact same origin (Scheme, Host, Port), verifying behavior with 
    different header casing.
    """
    session = Session()
    session.trust_env = False

    # Original request
    original_req = PreparedRequest()
    original_req.url = "http://example.com:8080/page1"
    
    response = Response()
    response.request = original_req

    # New request (same scheme, host, and port; different path)
    redirected_req = PreparedRequest()
    redirected_req.url = "http://example.com:8080/page2"
    
    auth_value = "Basic dXNlcjpwYXNz"
    redirected_req.headers = CaseInsensitiveDict({
        header_case: auth_value,
        "Accept": "text/html"
    })

    # Execute
    session.rebuild_auth(redirected_req, response)

    # Verify Authorization is preserved
    assert "Authorization" in redirected_req.headers
    assert redirected_req.headers["Authorization"] == auth_value
    assert redirected_req.headers["Accept"] == "text/html"