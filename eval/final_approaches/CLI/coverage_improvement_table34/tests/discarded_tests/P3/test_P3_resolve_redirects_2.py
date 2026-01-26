import pytest
from requests.sessions import SessionRedirectMixin
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from requests.exceptions import TooManyRedirects
from unittest.mock import Mock

def test_resolve_redirects_loop():
    mixin = SessionRedirectMixin()
    mixin.max_redirects = 2
    mixin.rebuild_method = Mock()
    mixin.rebuild_proxies = Mock(return_value={})
    mixin.rebuild_auth = Mock()
    mixin.cookies = RequestsCookieJar()
    
    req = PreparedRequest()
    req.url = "http://example.com/loop"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/loop"}
    resp.url = "http://example.com/loop"
    resp.request = req
    resp.raw = Mock()
    resp.raw.headers = {}
    # History length >= max_redirects triggers error
    resp.history = []
    
    # We need to loop. mixin.send must return a redirect response.
    redirect_resp = Mock()
    redirect_resp.is_redirect = True
    redirect_resp.status_code = 301
    redirect_resp.headers = {"location": "http://example.com/loop"}
    redirect_resp.url = "http://example.com/loop"
    redirect_resp.raw = Mock()
    redirect_resp.raw.headers = {}
    
    mixin.send = Mock(return_value=redirect_resp)
    
    with pytest.raises(TooManyRedirects):
        list(mixin.resolve_redirects(resp, req))