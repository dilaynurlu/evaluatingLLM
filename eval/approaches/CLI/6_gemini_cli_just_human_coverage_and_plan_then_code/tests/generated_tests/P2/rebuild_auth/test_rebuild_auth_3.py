import pytest
from unittest.mock import Mock, patch
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
    def should_strip_auth(self, old_url, new_url):
        return True

def test_rebuild_auth_netrc():
    session = DummySession()
    
    prep = Mock()
    prep.headers = {}
    prep.url = "http://example.com"
    
    resp = Mock()
    resp.request.url = "http://other.com"
    
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        mock_netrc.return_value = ("user", "pass")
        session.rebuild_auth(prep, resp)
        
        prep.prepare_auth.assert_called_with(("user", "pass"))
