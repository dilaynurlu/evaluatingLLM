import pytest
from requests.sessions import SessionRedirectMixin
from requests.exceptions import TooManyRedirects
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

def test_resolve_redirects_yield_requests():
    """Test yield_requests=True yields the Request object."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    
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
    
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    
    # It yields the request and then loops infinitely if we don't stop it (as resp isn't updated)
    # We just want to verify it yields the expected request.
    result = next(gen)
    
    assert result == cloned_req
    assert result.url == "http://example.com/2"
