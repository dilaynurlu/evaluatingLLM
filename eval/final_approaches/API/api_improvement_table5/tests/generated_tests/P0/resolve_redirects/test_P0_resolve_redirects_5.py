import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_fragment_inheritance():
    """
    Test fragment handling according to RFC 7231.
    If the original URL has a fragment and the redirect location does NOT,
    the original fragment should be preserved.
    """
    session = Session()
    
    # Original URL has a fragment
    req = Request('GET', 'http://example.com/page#section1').prepare()
    
    # Redirect location has NO fragment
    resp_redirect = Response()
    resp_redirect.status_code = 302
    resp_redirect.headers['Location'] = 'http://example.com/other'
    resp_redirect.url = 'http://example.com/page'
    resp_redirect.request = req
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = Mock()

    resp_target = Response()
    resp_target.status_code = 200
    resp_target.url = 'http://example.com/other#section1' # Expected result
    resp_target._content = b"ok"
    resp_target._content_consumed = True
    resp_target.raw = Mock()

    with patch.object(session, 'send', return_value=resp_target) as mock_send:
        gen = session.resolve_redirects(resp_redirect, req)
        next(gen)
        
        args, _ = mock_send.call_args
        sent_request = args[0]
        
        # The fragment #section1 should be appended
        assert sent_request.url == 'http://example.com/other#section1'