import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_resolve_redirects_simple_success():
    session = Session()
    
    # Setup original request
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url='http://example.com/one',
        headers={}
    )
    
    # Setup initial response triggering redirect
    resp1 = Response()
    resp1.url = 'http://example.com/one'
    resp1.status_code = 301
    resp1.headers = {'Location': 'http://example.com/two'}
    # Pre-consume content to avoid I/O
    resp1._content = b""
    resp1._content_consumed = True
    # Avoid cookie extraction issues
    resp1.raw = MagicMock()
    del resp1.raw._original_response

    # Setup the response that will be returned by the redirect
    resp2 = Response()
    resp2.url = 'http://example.com/two'
    resp2.status_code = 200
    resp2._content = b"Success"
    resp2._content_consumed = True
    resp2.raw = MagicMock()
    del resp2.raw._original_response

    # Patch send to return the second response
    with patch.object(Session, 'send', return_value=resp2) as mock_send:
        # Patch cookie extraction to avoid complex mock setup for internal structures
        with patch('requests.sessions.extract_cookies_to_jar'):
            
            gen = session.resolve_redirects(resp1, req)
            results = list(gen)
            
            # Should yield exactly one response
            assert len(results) == 1
            assert results[0] is resp2
            
            # Verify send was called with the redirect URL
            mock_send.assert_called_once()
            args, _ = mock_send.call_args
            sent_req = args[0]
            assert sent_req.url == 'http://example.com/two'
            
            # Verify history was updated
            assert len(resp2.history) == 1
            assert resp2.history[0] is resp1


'''
Assertion failed:

gen = session.resolve_redirects(resp1, req)
                results = list(gen)
    
                # Should yield exactly one response
>               assert len(results) == 1
E               assert 0 == 1
E                +  where 0 = len([])

eval/tests/generated_tests/P1/resolve_redirects/test_P1_resolve_redirects_1.py:47: AssertionError
'''