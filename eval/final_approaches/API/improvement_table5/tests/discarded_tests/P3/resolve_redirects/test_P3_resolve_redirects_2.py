import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects
from unittest.mock import MagicMock

def test_resolve_redirects_exceeds_max_redirects():
    """
    Test that TooManyRedirects is raised when the number of redirects exceeds session.max_redirects.
    Ensures that response history is tracked correctly up to the failure.
    """
    session = Session()
    session.max_redirects = 1
    
    url1 = "http://example.com/1"
    url2 = "http://example.com/2"
    url3 = "http://example.com/3"
    
    req = Request("GET", url1).prepare()
    
    # First response (Redirect 1 -> 2)
    resp1 = Response()
    resp1.request = req
    resp1.url = url1
    resp1.status_code = 302
    resp1.headers["Location"] = url2
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    # Second response (Redirect 2 -> 3)
    resp2 = Response()
    resp2.request = req.copy()
    resp2.request.url = url2
    resp2.url = url2
    resp2.status_code = 302
    resp2.headers["Location"] = url3
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = MagicMock()
    
    # Mock send to return resp2 when called
    session.send = MagicMock(return_value=resp2)
    
    # Generator execution
    gen = session.resolve_redirects(resp1, req)
    
    # First iteration should yield resp2 (the result of following the first redirect)
    yielded_resp = next(gen)
    assert yielded_resp == resp2
    assert yielded_resp.history[0] == resp1
    
    # Second iteration tries to follow redirect from resp2 -> url3
    # Logic:
    # 1. Check max_redirects (current history len is 1: [resp1])
    # 2. Prepare request for url3
    # 3. Send request -> get resp3 (not mocked yet, but doesn't matter because we check check before send? 
    #    Actually requests checks 'if len(resp.history) >= self.max_redirects' inside the loop logic or before yielding.
    #    Wait, the check usually happens *after* receiving a response that *is* a redirect.
    #    The yielded_resp IS a redirect (302). So we enter the loop again.
    #    The loop accumulates history. 
    #    If we call next(gen), it attempts to resolve the redirect in yielded_resp.
    
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)