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

def test_resolve_redirects_proxies_rebuild():
    """Test that proxies are rebuilt."""
    session = MockSession()
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/2"}
    resp.history = []
    resp.raw = Mock()
    
    req = Mock()
    req.url = "http://example.com/1"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    cloned_req = Mock()
    cloned_req.url = "http://example.com/2" # Should be updated
    cloned_req.headers = {}
    cloned_req._cookies = RequestsCookieJar()
    cloned_req.prepare_cookies = Mock()
    cloned_req.prepare_auth = Mock()
    
    req.copy = Mock(return_value=cloned_req)
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.history = []
    session.send.return_value = new_resp
    
    input_proxies = {"http": "http://proxy"}
    list(session.resolve_redirects(resp, req, proxies=input_proxies))
    
    # Check that session.send was called with proxies.
    # Since rebuild_proxies is real, it will return a dict.
    # If trust_env is True, it will check env. Assuming empty env, it should return input proxies.
    # SessionRedirectMixin.rebuild_proxies calls resolve_proxies.
    args, kwargs = session.send.call_args
    assert "proxies" in kwargs
    # We verify that proxies were passed.
    assert kwargs["proxies"]["http"] == "http://proxy"
