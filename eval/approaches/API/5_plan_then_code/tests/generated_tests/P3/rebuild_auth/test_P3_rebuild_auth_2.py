import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_preserves_credentials_on_same_origin():
    """
    Refined test: Verifies that Authorization headers are preserved when 
    redirecting to the exact same scheme, host, and port.
    
    Improvements:
    - Uses strict same-origin URLs (HTTPS -> HTTPS).
    - Uses dynamic credential generation (_basic_auth_str) to avoid hardcoded base64.
    """
    session = Session()
    session.trust_env = False

    # Generate credentials dynamically
    auth_val = _basic_auth_str('user', 'p@ssword123')

    # Original request
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "https://example.com/old-path"

    # New request (Redirect target) to same origin
    prep = PreparedRequest()
    prep.url = "https://example.com/new-path"
    
    prep.headers = requests.structures.CaseInsensitiveDict({
        "Authorization": auth_val
    })

    # Execute
    session.rebuild_auth(prep, resp)

    # Assert
    assert "Authorization" in prep.headers
    assert prep.headers["Authorization"] == auth_val