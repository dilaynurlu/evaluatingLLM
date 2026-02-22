from requests.sessions import SessionRedirectMixin
from requests.exceptions import TooManyRedirects
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock
import pytest

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 2
        self.cookies = RequestsCookieJar()
        self.trust_env = True
        self.proxies = {}
        self.auth = None
        self.stream = False
        self.verify = True
        self.cert = None
        self.hooks = {'response': []}
    
    rebuild_auth = Mock()
    rebuild_proxies = Mock(return_value={})
    rebuild_method = Mock()
    get_adapter = Mock()
    merge_environment_settings = Mock(return_value={})

    def send(self, request, **kwargs):
        # Always redirect
        r = Response()
        r.status_code = 302
        r.headers = {'location': 'http://example.com/next'}
        r.url = request.url
        r.request = request
        r.connection = Mock()
        r.raw = Mock()
        r.raw.stream.return_value = iter([b""])
        return r

def test_resolve_redirects_2():
    session = MockSession()
    
    resp = Response()
    resp.status_code = 302
    resp.headers = {'location': 'http://example.com/1'}
    resp.url = 'http://example.com/0'
    resp.request = PreparedRequest()
    resp.request._cookies = RequestsCookieJar()
    resp.request.url = 'http://example.com/0'
    resp.request.method = 'GET'
    resp.request.headers = {}
    resp.connection = Mock()
    resp.raw = Mock()
    resp.raw.stream.return_value = iter([b""])

    gen = session.resolve_redirects(resp, resp.request)
    
    with pytest.raises(TooManyRedirects):
        list(gen)
