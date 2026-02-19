import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_yield_requests_true():
    """
    Test usage of yield_requests=True.
    Verifies that the generator yields a PreparedRequest object instead of
    performing the request and yielding a Response.
    """
    session = Session()
    
    req = Request('GET', 'http://example.com/start').prepare()
    
    resp_redirect = Response()
    resp_redirect.status_code = 302
    resp_redirect.headers['Location'] = 'http://example.com/next'
    resp_redirect.url = 'http://example.com/start'
    resp_redirect.request = req
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = Mock()

    # Call with yield_requests=True
    gen = session.resolve_redirects(resp_redirect, req, yield_requests=True)
    
    # Expect a PreparedRequest
    result = next(gen)
    
    assert isinstance(result, PreparedRequest)
    assert result.url == 'http://example.com/next'
    
    # Ensure Session.send was NOT called
    with patch.object(session, 'send') as mock_send:
        # We need to re-create the generator to test the call behavior cleanly
        gen2 = session.resolve_redirects(resp_redirect, req, yield_requests=True)
        next(gen2)
        mock_send.assert_not_called()