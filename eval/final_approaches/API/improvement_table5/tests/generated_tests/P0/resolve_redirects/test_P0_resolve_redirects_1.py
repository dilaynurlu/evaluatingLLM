import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_simple_302():
    """
    Test a simple 302 Found redirect scenario.
    Verifies that the generator yields the response from the redirected URL
    and that the correct URL is requested.
    """
    session = Session()
    
    # Setup initial request and response
    req = Request('GET', 'http://example.com/original').prepare()
    
    resp_redirect = Response()
    resp_redirect.status_code = 302
    resp_redirect.headers['Location'] = 'http://example.com/target'
    resp_redirect.url = 'http://example.com/original'
    resp_redirect.request = req
    resp_redirect.reason = 'Found'
    # Mock content/raw to avoid I/O
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = Mock()

    # Setup the response for the redirect target
    resp_target = Response()
    resp_target.status_code = 200
    resp_target.url = 'http://example.com/target'
    resp_target.request = Request('GET', 'http://example.com/target').prepare()
    resp_target._content = b"Target Content"
    resp_target._content_consumed = True
    resp_target.raw = Mock()

    # Mock Session.send to return the target response
    with patch.object(session, 'send', return_value=resp_target) as mock_send:
        # Execute
        gen = session.resolve_redirects(resp_redirect, req)
        result_resp = next(gen)
        
        # Verify the yielded response is the target response
        assert result_resp is resp_target
        assert result_resp.status_code == 200
        assert result_resp.url == 'http://example.com/target'
        
        # Verify Session.send was called with the correct URL
        args, _ = mock_send.call_args
        sent_request = args[0]
        assert sent_request.url == 'http://example.com/target'
        assert sent_request.method == 'GET'
        
        # Verify generator is exhausted (assuming no further redirects)
        with pytest.raises(StopIteration):
            next(gen)