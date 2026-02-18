import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock
from requests.cookies import RequestsCookieJar

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 5
        self.cookies = RequestsCookieJar()
        self.trust_env = True
        self.proxies = {}
        self.auth = None
        self.headers = {}
        self.send = Mock()

def test_resolve_redirects_stop_on_no_url():
    """Test that generator stops when get_redirect_target returns None."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = False # This causes get_redirect_target to return None
    resp.history = []
    
    req = Mock()
    req.url = "http://example.com/1"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req.copy = Mock(return_value=req)
    
    results = list(session.resolve_redirects(resp, req))
    assert len(results) == 0
