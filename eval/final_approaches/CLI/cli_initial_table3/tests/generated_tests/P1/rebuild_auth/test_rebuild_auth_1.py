from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock, patch

def test_rebuild_auth_strip():
    session = Session()
    # Mock should_strip_auth to return True
    session.should_strip_auth = MagicMock(return_value=True)
    session.trust_env = False # disable netrc for this test

    # Prepared request with Authorization header
    prep = PreparedRequest()
    prep.url = "http://new-domain.com"
    prep.headers = {"Authorization": "Basic user:pass"}
    
    # Response from previous request
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://old-domain.com"
    
    session.rebuild_auth(prep, resp)
    
    assert "Authorization" not in prep.headers
    session.should_strip_auth.assert_called_with("http://old-domain.com", "http://new-domain.com")
