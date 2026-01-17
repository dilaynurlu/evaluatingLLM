import pytest
from unittest.mock import Mock
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
    def should_strip_auth(self, old_url, new_url):
        return False

def test_rebuild_auth_keep():
    session = DummySession()
    
    prep = Mock()
    prep.headers = {"Authorization": "Basic ..."}
    prep.url = "http://same.com"
    prep.prepare_auth = Mock()
    
    resp = Mock()
    resp.request.url = "http://same.com"
    
    session.rebuild_auth(prep, resp)
    
    assert "Authorization" in prep.headers
