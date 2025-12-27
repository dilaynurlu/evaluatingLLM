import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_resolve_redirects_yield_requests():
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/start')
    
    resp = Response()
    resp.url = 'http://example.com/start'
    resp.status_code = 302
    resp.headers = {'Location': 'http://example.com/next'}
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    del resp.raw._original_response

    with patch.object(Session, 'send') as mock_send:
        with patch('requests.sessions.extract_cookies_to_jar'):
            
            # yield_requests=True
            gen = session.resolve_redirects(resp, req, yield_requests=True)
            results = list(gen)
            
            # Should yield a PreparedRequest, not a Response
            assert len(results) == 1
            assert isinstance(results[0], PreparedRequest)
            assert results[0].url == 'http://example.com/next'
            
            # Send should NOT be called when yielding requests
            mock_send.assert_not_called()

'''
Assertion failed:

assert len(results) == 1
E               assert 0 == 1
E                +  where 0 = len([])

eval/tests/generated_tests/P1/resolve_redirects/test_P1_resolve_redirects_3.py:29: AssertionError
'''