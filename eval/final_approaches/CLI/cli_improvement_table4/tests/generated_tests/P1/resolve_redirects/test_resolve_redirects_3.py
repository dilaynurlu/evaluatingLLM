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

def test_resolve_redirects_relative_url():
    """Test resolving relative redirect URL."""
    session = MockSession()
    
    resp = Mock()
    resp.url = "http://example.com/foo/bar"
    resp.is_redirect = True
    resp.status_code = 301
    # Real get_redirect_target uses this header
    resp.headers = {"location": "../baz"}
    resp.history = []
    
    req = Mock()
    req.url = "http://example.com/foo/bar"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    # We need a robust copy mock to capture the mutated request
    cloned_req = Mock()
    cloned_req.headers = {}
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    
    def side_effect_copy():
        return cloned_req
    req.copy = side_effect_copy
    
    # Stop the loop after one redirect
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    list(session.resolve_redirects(resp, req))
    
    # Check that req.url was updated correctly in the clone
    # urljoin('http://example.com/foo/bar', '../baz') -> 'http://example.com/baz'
    assert cloned_req.url == "http://example.com/baz"
