from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock

def test_rebuild_auth_keep():
    session = Session()
    # Mock should_strip_auth to return False
    session.should_strip_auth = MagicMock(return_value=False)
    session.trust_env = False

    # Prepared request with Authorization header
    prep = PreparedRequest()
    prep.url = "http://same-domain.com"
    prep.headers = {"Authorization": "Basic user:pass"}
    
    # Response from previous request
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = "http://same-domain.com"
    
    session.rebuild_auth(prep, resp)
    
    assert "Authorization" in prep.headers
    assert prep.headers["Authorization"] == "Basic user:pass"
