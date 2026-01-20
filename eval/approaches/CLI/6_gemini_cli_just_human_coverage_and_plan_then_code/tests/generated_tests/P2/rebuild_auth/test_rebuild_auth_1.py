import pytest
from unittest.mock import Mock
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
    def should_strip_auth(self, old_url, new_url):
        return True

def test_rebuild_auth_strip():
    session = DummySession()
    
    # Prepared Request
    prep = Mock()
    prep.headers = {"Authorization": "Basic ..."}
    prep.url = "http://new.com"
    
    # Response
    resp = Mock()
    resp.request.url = "http://old.com"
    
    session.rebuild_auth(prep, resp)
    
    assert "Authorization" not in prep.headers
