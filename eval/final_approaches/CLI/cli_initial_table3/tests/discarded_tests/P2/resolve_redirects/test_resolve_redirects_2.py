import pytest
from unittest.mock import MagicMock
from requests.sessions import SessionRedirectMixin
from requests.exceptions import TooManyRedirects
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_too_many_redirects():
    """
    Test TooManyRedirects exception.
    """
    mixin = SessionRedirectMixin()
    mixin.max_redirects = 1
    mixin.trust_env = False
    
    # Mock methods
    mixin.rebuild_method = MagicMock()
    mixin.rebuild_proxies = MagicMock(return_value={})
    mixin.rebuild_auth = MagicMock()
    mixin.cookies = RequestsCookieJar()
    
    # Initial response (1st redirect)
    resp1 = MagicMock()
    resp1.is_redirect = True
    resp1.status_code = 301
    resp1.headers = {"location": "/1"}
    resp1.history = []
    resp1.url = "http://example.com/0"
    
    req = MagicMock()
    req.url = "http://example.com/0"
    req._cookies = RequestsCookieJar()
    req.copy.return_value = req
    
    # Second response (2nd redirect)
    resp2 = MagicMock()
    resp2.is_redirect = True
    resp2.status_code = 301
    resp2.headers = {"location": "/2"}
    resp2.history = [resp1]
    resp2.url = "http://example.com/1"
    
    # Third response (3rd redirect)
    resp3 = MagicMock()
    resp3.is_redirect = True
    resp3.status_code = 301
    resp3.headers = {"location": "/3"}
    resp3.history = [resp1, resp2]
    resp3.url = "http://example.com/2"
    
    # Mock send sequence
    mixin.send = MagicMock(side_effect=[resp2, resp3])
    
    gen = mixin.resolve_redirects(resp1, req)
    
    # Should yield resp2 then raise on next iteration
    next(gen) # Yields resp2
    
    with pytest.raises(TooManyRedirects):
        next(gen)