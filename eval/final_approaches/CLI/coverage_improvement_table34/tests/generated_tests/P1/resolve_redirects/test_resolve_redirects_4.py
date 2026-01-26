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

def test_resolve_redirects_scheme_relative():
    """Test resolving scheme-relative redirect URL (//example.com)."""
    session = MockSession()
    
    resp = Mock()
    resp.url = "https://example.com/1"
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "//other.com/2"}
    resp.history = []
    
    req = Mock()
    req.url = "https://example.com/1"
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
    
    list(session.resolve_redirects(resp, req))
    
    # Should inherit scheme from resp.url (https)
    assert cloned_req.url == "https://other.com/2"
