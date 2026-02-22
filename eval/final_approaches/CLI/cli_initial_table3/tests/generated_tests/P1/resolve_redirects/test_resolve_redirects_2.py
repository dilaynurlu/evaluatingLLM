from requests.sessions import Session
from requests.exceptions import TooManyRedirects
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock

def test_resolve_redirects_max_limit():
    session = Session()
    session.max_redirects = 2
    
    session.get_redirect_target = MagicMock(return_value="http://example.com/loop")
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    session.send = MagicMock()
    
    req = PreparedRequest()
    req.url = "http://example.com"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    resp = Response()
    resp.request = req
    resp.status_code = 302
    resp.url = "http://example.com"
    resp.raw = MagicMock()
    resp.close = MagicMock()
    resp.history = []
    
    # Simulate first redirect
    resp1 = Response()
    resp1.request = req
    resp1.status_code = 302
    resp1.url = "http://example.com/loop"
    resp1.raw = MagicMock()
    resp1.history = [resp]
    
    # Simulate second redirect
    resp2 = Response()
    resp2.request = req
    resp2.status_code = 302
    resp2.url = "http://example.com/loop"
    resp2.raw = MagicMock()
    resp2.history = [resp, resp1]
    
    # Simulate third redirect (should fail)
    resp3 = Response()
    resp3.request = req
    resp3.status_code = 302
    resp3.url = "http://example.com/loop"
    resp3.raw = MagicMock()
    resp3.history = [resp, resp1, resp2]
    
    session.send.side_effect = [resp1, resp2, resp3]
    
    gen = session.resolve_redirects(resp, req)
    
    try:
        next(gen) # Yields resp1
        next(gen) # Yields resp2
        next(gen) # Should raise TooManyRedirects because len(history) >= max_redirects
        assert False, "Should raise TooManyRedirects"
    except TooManyRedirects:
        pass
