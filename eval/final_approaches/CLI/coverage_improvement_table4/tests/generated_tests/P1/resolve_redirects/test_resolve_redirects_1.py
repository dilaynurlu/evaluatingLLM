import pytest
from requests.sessions import SessionRedirectMixin
from requests.exceptions import TooManyRedirects
from unittest.mock import Mock, MagicMock
from requests.cookies import RequestsCookieJar

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.cookies = RequestsCookieJar()
        self.trust_env = True
        self.proxies = {}
        self.auth = None
        self.headers = {}
        # We strictly mock send because it does network IO
        self.send = Mock()

def test_resolve_redirects_single_redirect():
    """Test a single successful redirect using real mixin methods."""
    session = MockSession()
    
    # Initial response
    resp = Mock()
    resp.is_redirect = True
    resp.url = "http://example.com/1"
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    resp.raw = Mock() # needed for cookie extraction (mocked)
    
    # Request setup
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    # When copy() is called, we return a new Mock to simulate a new request object
    # We need to preserve attributes or at least structure
    def side_effect_copy():
        new_req = Mock()
        new_req.url = req.url
        new_req.method = req.method
        new_req.headers = req.headers.copy()
        new_req._cookies = RequestsCookieJar()
        new_req._body_position = None
        new_req.copy = side_effect_copy
        new_req.prepare_cookies = Mock()
        new_req.prepare_auth = Mock()
        return new_req
        
    req.copy = side_effect_copy
    
    # Mock send to return a new response that is NOT a redirect
    new_resp = Mock()
    new_resp.url = "http://example.com/2"
    new_resp.history = [resp]
    new_resp.is_redirect = False 
    new_resp.status_code = 200
    new_resp.headers = {}
    new_resp.raw = Mock()
    
    # The session.send will be called with the *new* request object (from copy)
    session.send.return_value = new_resp
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    results = list(gen)
    
    assert len(results) == 1
    assert results[0] == new_resp
    
    # Verify session.send was called
    assert session.send.call_count == 1
    # Check that the URL was updated in the request passed to send
    args, _ = session.send.call_args
    sent_request = args[0]
    assert sent_request.url == "http://example.com/2"