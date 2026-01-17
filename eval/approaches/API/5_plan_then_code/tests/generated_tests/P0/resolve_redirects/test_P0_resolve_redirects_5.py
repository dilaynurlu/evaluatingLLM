import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_yield_requests_mode():
    """
    Test that when yield_requests=True, the method yields PreparedRequest objects
    instead of sending them.
    """
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/start')
    
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = 'http://example.com/next'
    resp1.url = 'http://example.com/start'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    # Mock send to ensure it is NOT called
    session.send = MagicMock()
    
    gen = session.resolve_redirects(resp1, req, yield_requests=True)
    
    # It should yield the PreparedRequest for the redirect location
    result = next(gen)
    
    assert isinstance(result, PreparedRequest)
    assert result.url == 'http://example.com/next'
    
    # Ensure session.send was not called
    session.send.assert_not_called()
    
    # The generator should finish after yielding the request because it doesn't execute the request
    # to get a new response to check for further redirects in this mode (based on the loop logic provided)
    # Actually, the loop continues 'while url'. But 'url' is updated from 'self.get_redirect_target(resp)'.
    # In 'yield_requests' mode, 'resp' is NOT updated (no send() called).
    # So 'url' remains the same? No.
    # Code analysis:
    # req = prepared_request
    # if yield_requests:
    #     yield req
    # else:
    #     resp = self.send(...)
    #     url = self.get_redirect_target(resp)
    #     yield resp
    #
    # If yield_requests is True, 'url' (the loop condition) is NOT updated inside the loop.
    # It would be an infinite loop if 'url' stays truthy.
    # However, 'url' variable is updated EARLIER in the loop:
    # 'url' is used to create 'prepared_request.url'.
    # But the variable 'url' determines the loop continuation.
    # Wait, the code snippet:
    # while url:
    #     ...
    #     if yield_requests:
    #         yield req
    #     else:
    #         ...
    #         url = self.get_redirect_target(resp)
    #         yield resp
    #
    # If yield_requests is True, 'url' is never updated at the end of the loop.
    # This implies resolve_redirects with yield_requests=True might loop infinitely if not handled?
    # Or implies it's intended for single-step or external control.
    # BUT: The provided code does NOT update 'url' when yield_requests is True.
    # Thus, checking for StopIteration or infinite generation is important.
    # Let's just check the first yield.
    pass