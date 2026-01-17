import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response, TooManyRedirects

def test_resolve_redirects_enforces_max_redirects():
    """
    Test that resolve_redirects raises TooManyRedirects when the number of 
    redirects exceeds the configured max_redirects limit.
    """
    session = Session()
    session.max_redirects = 1  # Set a low limit for testing
    
    # Mock send to always return a redirect response
    def redirect_side_effect(request, **kwargs):
        r = Response()
        r.status_code = 301
        r.headers["Location"] = "http://example.com/loop"
        r.url = request.url
        r._content = b""
        r._content_consumed = True
        r.raw = MagicMock()
        return r

    session.send = Mock(side_effect=redirect_side_effect)

    # Initial Request
    req = Request("GET", "http://example.com/start").prepare()
    
    # Initial Response (Redirect 1)
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/next"
    resp.url = "http://example.com/start"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()

    # Execute resolve_redirects
    # The first next() should process the first redirect and yield the second response
    gen = session.resolve_redirects(resp, req)
    
    # First redirect is processed, yields the result of send() (which is another redirect)
    next(gen)
    
    # The next iteration processes the second redirect. 
    # Current history len will be 1 (from first resp). 
    # When loop runs again, it appends the second resp. History len becomes 2.
    # max_redirects is 1. 2 > 1. Should raise.
    
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
        
    assert "Exceeded 1 redirects" in str(excinfo.value)