import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, Request
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session's max_redirects setting.
    """
    session = Session()
    session.max_redirects = 1
    
    # Initial request
    req = Request('GET', 'http://example.com/1')
    prep_req = session.prepare_request(req)
    
    # First response (302 Redirect to /2)
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = 'http://example.com/2'
    resp1.url = 'http://example.com/1'
    resp1.request = prep_req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    # Second response (302 Redirect to /3) - This should trigger the limit
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers['Location'] = 'http://example.com/3'
    resp2.url = 'http://example.com/2'
    resp2.request = None 
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = MagicMock()

    # Third response (should not be reached if limit works)
    resp3 = Response()
    resp3.status_code = 200
    resp3.url = 'http://example.com/3'
    resp3.raw = MagicMock()
    
    # Configure mock to return resp2 then resp3
    session.send = Mock(side_effect=[resp2, resp3])
    
    gen = session.resolve_redirects(resp1, prep_req)
    
    # The first yield is the result of following the first redirect (resp2)
    first_yield = next(gen)
    assert first_yield.url == 'http://example.com/2'
    
    # The next iteration attempts to follow the redirect from resp2
    # Since max_redirects is 1, and we are now on the 2nd redirect, it should raise
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)