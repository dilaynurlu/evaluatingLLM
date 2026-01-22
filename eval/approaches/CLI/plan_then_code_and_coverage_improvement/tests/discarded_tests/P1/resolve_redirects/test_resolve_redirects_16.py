import pytest
from requests.sessions import SessionRedirectMixin
from requests.exceptions import UnrewindableBodyError
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

def test_resolve_redirects_not_rewindable_no_content_length():
    """Test that UnrewindableBodyError is NOT raised if no Content-Length/Transfer-Encoding."""
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
    req.headers = {} # No Content-Length
    req._cookies = RequestsCookieJar()
    req._body_position = object() # Failed tell
    req.body = object()
    
    cloned_req = Mock()
    cloned_req.headers = req.headers.copy()
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    cloned_req._body_position = req._body_position
    cloned_req.body = req.body
    
    req.copy = Mock(return_value=cloned_req)
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    # Should not raise
    list(session.resolve_redirects(resp, req))
