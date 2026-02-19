import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_307_method_preserve():
    """
    Test a 307 Temporary Redirect.
    Verifies that the request method (POST) and body are preserved.
    """
    session = Session()
    
    # Setup initial POST request
    data_content = 'important_data'
    req = Request('POST', 'http://example.com/submit', data=data_content).prepare()
    
    # Setup 307 redirect response
    resp_redirect = Response()
    resp_redirect.status_code = 307
    resp_redirect.headers['Location'] = 'http://example.com/resubmit'
    resp_redirect.url = 'http://example.com/submit'
    resp_redirect.request = req
    resp_redirect.reason = 'Temporary Redirect'
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = Mock()

    # Setup target response
    resp_target = Response()
    resp_target.status_code = 200
    resp_target.url = 'http://example.com/resubmit'
    resp_target._content = b"ok"
    resp_target._content_consumed = True
    resp_target.raw = Mock()

    with patch.object(session, 'send', return_value=resp_target) as mock_send:
        gen = session.resolve_redirects(resp_redirect, req)
        next(gen)
        
        args, _ = mock_send.call_args
        sent_request = args[0]
        
        # Method must remain POST
        assert sent_request.method == 'POST'
        # Body must be preserved
        assert sent_request.body == data_content