import pytest
from unittest.mock import Mock, patch
from requests.sessions import SessionRedirectMixin

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = True
    def should_strip_auth(self, old_url, new_url):
        return True

def test_rebuild_auth_proxy_removal():
    # rebuild_auth doesn't remove Proxy-Authorization, but let's double check.
    # Ah, rebuild_proxies does that.
    # But rebuild_auth is what we are testing.
    # So we check that Proxy-Authorization is untouched by rebuild_auth.
    
    session = DummySession()
    prep = Mock()
    prep.headers = {"Proxy-Authorization": "Basic ...", "Authorization": "Basic ..."}
    prep.url = "http://new.com"
    resp = Mock()
    resp.request.url = "http://old.com"
    
    # It should strip Authorization but leave Proxy-Authorization (handled elsewhere)
    session.rebuild_auth(prep, resp)
    
    assert "Authorization" not in prep.headers
    assert "Proxy-Authorization" in prep.headers
