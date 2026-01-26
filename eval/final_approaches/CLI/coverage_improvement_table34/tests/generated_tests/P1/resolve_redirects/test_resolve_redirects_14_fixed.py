import pytest
from requests.sessions import SessionRedirectMixin
from unittest.mock import Mock, MagicMock, patch
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

class RealResponse:
    def __init__(self, headers, url, status_code=301, is_redirect=True):
        self.headers = headers
        self.is_redirect = is_redirect
        self.url = url
        self.status_code = status_code
        self.history = []
        self.raw = Mock()
        self.encoding = 'utf-8'
        self.content = b""
        self.request = Mock()
        self.request.url = url
    
    def close(self):
        pass

def test_resolve_redirects_history_update_fixed():
    """Test that history is updated correctly."""
    session = MockSession()
    
    # Resp 1 -> 2
    resp1 = RealResponse(headers={"location": "http://example.com/2"}, url="http://example.com/1")
    
    req = MagicMock()
    req.url = "http://example.com/1"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    # Clone 1
    req2 = MagicMock()
    req2.url = "http://example.com/2"
    req2.headers = {}
    req2._cookies = RequestsCookieJar()
    req2.prepare_cookies = Mock()
    req2.prepare_auth = Mock()
    
    # Clone 2
    req3 = MagicMock()
    req3.url = "http://example.com/3"
    req3.headers = {}
    req3._cookies = RequestsCookieJar()
    req3.prepare_cookies = Mock()
    req3.prepare_auth = Mock()
    
    req.copy = Mock(side_effect=[req2, req3])
    
    # Resp 2 -> 3
    resp2 = RealResponse(headers={"location": "http://example.com/3"}, url="http://example.com/2")
    
    # Resp 3 -> Done
    resp3 = RealResponse(headers={}, url="http://example.com/3", is_redirect=False, status_code=200)
    
    session.send.side_effect = [resp2, resp3]
    
    # Patch cookie functions to avoid failures
    with patch("requests.sessions.extract_cookies_to_jar"), \
         patch("requests.sessions.merge_cookies"):
    
        results = list(session.resolve_redirects(resp1, req))
    
    # Check history of yielded responses
    # First yield is resp2.
    assert len(resp2.history) == 1
    # Logic is resp.history = hist[1:]. hist=[resp1, resp2]. resp2.history=[resp2]
    assert resp2.history[0].url == resp2.url
    
    # Second yield is resp3.
    # resp3 returned by send. resolve_redirects does not update its history (loop ends).
    assert len(resp3.history) == 0
