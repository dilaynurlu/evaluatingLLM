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

def test_resolve_redirects_consume_content_error():
    """Test that content consumption errors are ignored."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    # Make resp.content raise RuntimeError
    type(resp).content = property(fget=Mock(side_effect=RuntimeError))
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    cloned_req = Mock()
    cloned_req.headers = {}
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    req.copy = Mock(return_value=cloned_req)
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    # Should not raise
    list(session.resolve_redirects(resp, req))
