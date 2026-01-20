from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_max_exceeded():
    s = Session()
    s.max_redirects = 1
    s.send = Mock()
    
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/1"
    resp.url = "http://example.com/0"
    
    req = PreparedRequest()
    req.url = "http://example.com/0"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    # Next response also redirects
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers["Location"] = "http://example.com/2"
    resp1.url = "http://example.com/1"
    
    s.send.side_effect = [resp1]
    
    gen = s.resolve_redirects(resp, req)
    
    # First yield is resp1. Next iteration checks max_redirects.
    # resp1.history will have 1 item.
    # loop checks if len(resp.history) >= self.max_redirects
    
    # We yield the response THEN check history?
    # No, code:
    # yield resp
    # (loop continues)
    # url = self.get_redirect_target(resp)
    # ...
    # hist.append(resp) ...
    # if len(resp.history) >= self.max_redirects: raise
    
    # So we get one response, then it tries next, finds max exceeded.
    
    iterator = iter(gen)
    assert next(iterator) == resp1
    
    try:
        next(iterator)
    except TooManyRedirects:
        pass
    else:
        assert False, "Should have raised TooManyRedirects"
