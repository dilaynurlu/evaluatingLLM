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

def test_resolve_redirects_purge_headers():
    """Test purging of headers on 303 redirect."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 303 # See Other -> changes to GET and drops body/headers
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "POST"
    # Using real dict for headers to test purging logic
    req.headers = {"Content-Length": "100", "Content-Type": "text/plain", "Transfer-Encoding": "chunked", "Keep-Alive": "True"}
    req.body = "some data"
    req._cookies = RequestsCookieJar()
    
    # Manual copy implementation
    cloned_req = Mock()
    cloned_req.headers = req.headers.copy()
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    cloned_req._body_position = None
    
    req.copy = Mock(return_value=cloned_req)
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    list(session.resolve_redirects(resp, req))
    
    assert "Content-Length" not in cloned_req.headers
    assert "Content-Type" not in cloned_req.headers
    assert "Transfer-Encoding" not in cloned_req.headers
    assert "Keep-Alive" in cloned_req.headers
    assert cloned_req.body is None
    assert cloned_req.method == "GET" # 303 changes method to GET
