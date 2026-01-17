import pytest
from unittest.mock import Mock
from requests.sessions import Session, TooManyRedirects
from requests.models import Response, PreparedRequest

def test_resolve_redirects_max_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects 
    exceeds session.max_redirects.
    """
    session = Session()
    session.max_redirects = 1
    
    # Setup a scenario where we have a chain of redirects
    # Chain: Start -> Redirect1 -> Redirect2 (Should Fail here if max=1)
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/0")
    
    # First response (triggers the resolution)
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers["Location"] = "http://example.com/1"
    resp1.url = "http://example.com/0"
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    
    # Second response (first yield, also a redirect)
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers["Location"] = "http://example.com/2"
    resp2.url = "http://example.com/1"
    resp2._content = b""
    resp2._content_consumed = True
    
    # Third response (should never be reached/yielded successfully if limit triggers)
    resp3 = Response()
    resp3.status_code = 200
    resp3.url = "http://example.com/2"
    resp3._content = b""
    resp3._content_consumed = True
    
    # Mock send to return resp2 then resp3
    session.send = Mock(side_effect=[resp2, resp3])
    
    # Execute
    gen = session.resolve_redirects(resp1, req)
    
    # The first iteration processes resp1. 
    # It yields resp2.
    # The user asks for the next item.
    # The second iteration processes resp2.
    # History now contains [resp1, resp2]. Length 2.
    # max_redirects is 1. 2 > 1. Should raise.
    
    # First yield should be fine (resp2)
    next(gen)
    
    # Second yield should raise
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
        
    assert "Exceeded 1 redirects" in str(excinfo.value)