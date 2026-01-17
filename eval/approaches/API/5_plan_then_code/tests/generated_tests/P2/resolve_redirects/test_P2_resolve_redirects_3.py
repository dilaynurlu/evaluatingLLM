import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_yield_requests():
    """
    Test that setting yield_requests=True yields the PreparedRequest object
    instead of sending it and yielding a Response.
    """
    session = Session()
    
    initial_url = 'http://example.com/start'
    target_url = 'http://example.com/next'
    req = Request('GET', initial_url).prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.url = initial_url
    resp.headers['Location'] = target_url
    resp._content = b''
    resp._content_consumed = True
    resp.request = req
    
    # Mock send to ensure it is NOT called
    session.send = Mock()
    
    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    
    # Get the first item yielded
    item = next(gen)
    
    # Verify it is a PreparedRequest
    assert isinstance(item, PreparedRequest)
    assert item.url == target_url
    
    # Verify session.send was not called
    session.send.assert_not_called()