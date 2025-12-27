import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_no_redirect():
    """
    Test scenario where the response status indicates success (200),
    so no redirect logic should be triggered.
    """
    session = Session()
    # Mock send to ensure no network requests are made
    session.send = MagicMock()
    
    # Create a real Response object
    resp = Response()
    resp.status_code = 200
    resp.url = "http://example.com"
    # Set content to empty bytes to signify it's consumed/safe to close
    resp._content = b""
    
    # Create a real PreparedRequest
    req = PreparedRequest()
    req.prepare(method='GET', url="http://example.com")
    
    # Execute resolve_redirects
    # Using the instance method directly
    gen = session.resolve_redirects(resp, req)
    results = list(gen)
    
    # Assertions
    assert results == []
    session.send.assert_not_called()
    
    # Note: Response.close() is called inside resolve_redirects only if a redirect happens.
    # Since the generator yields nothing, the loop doesn't start/continue, 
    # but the initial response handling (like history) isn't triggered.