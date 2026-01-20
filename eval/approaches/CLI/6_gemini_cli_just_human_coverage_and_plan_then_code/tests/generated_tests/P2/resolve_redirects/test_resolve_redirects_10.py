import pytest
from unittest.mock import Mock, patch
from requests.sessions import SessionRedirectMixin

from requests.cookies import RequestsCookieJar

class DummySession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 30
        self.trust_env = True
        self.auth = None
        self.proxies = {}
        self.cookies = RequestsCookieJar()
    def rebuild_method(self, prep, resp): pass
    def rebuild_proxies(self, prep, proxies): return proxies
    def rebuild_auth(self, prep, resp): pass

def test_resolve_redirects_cookies_merge():
    session = DummySession()
    req = Mock()
    req.url = "http://example.com"
    req.headers = {}
    req.copy.return_value = req
    req._cookies = RequestsCookieJar()
    
    resp = Mock()
    resp.is_redirect = True
    resp.url = "http://example.com"
    resp.history = []
    
    session.get_redirect_target = Mock(side_effect=["http://new.com", None])
    session.send = Mock(return_value=Mock(is_redirect=False))
    
    # We want to verify that extract_cookies_to_jar and merge_cookies are called
    with patch('requests.sessions.extract_cookies_to_jar') as mock_extract, \
         patch('requests.sessions.merge_cookies') as mock_merge:
        
        list(session.resolve_redirects(resp, req))
        
        assert mock_extract.called
        assert mock_merge.called
