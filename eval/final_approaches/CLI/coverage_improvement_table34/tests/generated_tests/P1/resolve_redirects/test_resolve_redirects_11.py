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

def test_resolve_redirects_cookies_handling():
    """Test that cookies are extracted and merged."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    resp.raw = Mock()
    # Mock cookiejar interaction if possible?
    # extract_cookies_to_jar calls cookiejar methods.
    # We can rely on RequestsCookieJar functioning (it's real code).
    
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "GET"
    req.headers = {"Cookie": "old_cookie=1"}
    req._cookies = RequestsCookieJar()
    
    cloned_req = Mock()
    cloned_req.headers = req.headers.copy()
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    
    req.copy = Mock(return_value=cloned_req)
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    list(session.resolve_redirects(resp, req))
    
    # Check that Cookie header is popped
    assert "Cookie" not in cloned_req.headers
    # Check that cookies were prepared (method called)
    cloned_req.prepare_cookies.assert_called()
