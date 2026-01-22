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

def test_resolve_redirects_unrewindable_body():
    """Test raising UnrewindableBodyError if body cannot be rewound."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 307 # Redirects maintaining method/body
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "POST"
    req.headers = {"Content-Length": "10"}
    req._cookies = RequestsCookieJar()
    req._body_position = object() # Indicates failed tell() -> rewindable=True logic trigger
    req.body = object() # No seek method
    
    cloned_req = Mock()
    cloned_req.headers = req.headers.copy()
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    # Copied request inherits _body_position? 
    # Logic: prepared_request = req.copy()... 
    # prepared_request._body_position is accessed.
    # We must ensure cloned_req has it.
    cloned_req._body_position = req._body_position
    cloned_req.body = req.body
    
    req.copy = Mock(return_value=cloned_req)
    
    with pytest.raises(UnrewindableBodyError):
        list(session.resolve_redirects(resp, req))
