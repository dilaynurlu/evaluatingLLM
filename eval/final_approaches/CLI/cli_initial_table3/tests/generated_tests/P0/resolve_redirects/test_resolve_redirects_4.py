from requests.sessions import SessionRedirectMixin
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.max_redirects = 3
        self.cookies = RequestsCookieJar()
        self.trust_env = True
        self.auth = None
        self.proxies = {}
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
        r = Response()
        r.status_code = 200
        r.url = request.url
        r.request = request
        r.connection = Mock()
        r.raw = Mock()
        r.raw.stream.return_value = iter([b""])
        return r

def test_resolve_redirects_4():
    session = MockSession()
    
    # URL with fragment, redirect location without fragment -> keep original fragment
    resp = Response()
    resp.status_code = 302
    resp.headers = {'location': 'http://example.com/new'}
    resp.url = 'http://example.com/old#frag'
    resp.request = PreparedRequest()
    resp.request._cookies = RequestsCookieJar()
    resp.request.url = 'http://example.com/old#frag'
    resp.request.method = 'GET'
    resp.request.headers = {}
    resp.connection = Mock()
    resp.raw = Mock()
    resp.raw.stream.return_value = iter([b""])
    
    gen = session.resolve_redirects(resp, resp.request)
    history = list(gen)
    
    assert len(history) == 1
    # Check if fragment preserved
    assert history[0].url == 'http://example.com/new#frag'
