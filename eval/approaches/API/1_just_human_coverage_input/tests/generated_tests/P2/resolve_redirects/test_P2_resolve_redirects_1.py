import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_basic_301_redirect():
    """
    Test a simple 301 Moved Permanently redirect.
    Verifies that the function follows the redirect, updates the URL,
    calls session.send with the new request, and yields the final response.
    """
    session = Session()
    
    # Original Request
    req = Request('GET', 'http://example.com/source').prepare()
    
    # Initial Response (301)
    resp = Response()
    resp.status_code = 301
    resp.url = 'http://example.com/source'
    resp.headers = CaseInsensitiveDict({'Location': 'http://example.com/target'})
    resp.request = req
    resp.raw = MagicMock()  # Mock raw to allow content consumption check
    
    # Next Response (200) - to be returned by session.send
    next_resp = Response()
    next_resp.status_code = 200
    next_resp.url = 'http://example.com/target'
    next_resp.request = None 
    
    # Mock send to return the 200 OK response
    session.send = Mock(return_value=next_resp)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    result = next(gen)
    
    # Assert correct response yielded
    assert result.status_code == 200
    assert result.url == 'http://example.com/target'
    
    # Assert session.send was called with correct URL
    session.send.assert_called_once()
    args, _ = session.send.call_args
    sent_request = args[0]
    assert sent_request.url == 'http://example.com/target'
    assert sent_request.method == 'GET'
    
    # Ensure generator is exhausted (loop terminates as 200 is not a redirect)
    with pytest.raises(StopIteration):
        next(gen)