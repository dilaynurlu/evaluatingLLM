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

def test_resolve_redirects_rewind_body_success():
    """Test successful rewinding of body."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 307
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "POST"
    req.headers = {"Content-Length": "10"}
    req._body_position = 0
    req._cookies = RequestsCookieJar()
    req.body = Mock() # Has seek
    
    cloned_req = Mock()
    cloned_req.headers = req.headers.copy()
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    cloned_req._body_position = 0
    cloned_req.body = req.body
    
    req.copy = Mock(return_value=cloned_req)
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    list(session.resolve_redirects(resp, req))
    
    req.body.seek.assert_called_with(0)
