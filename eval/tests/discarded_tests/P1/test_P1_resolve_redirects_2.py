import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_limit_exceeded():
    session = Session()
    session.max_redirects = 2
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/start')
    
    # Initial response
    resp = Response()
    resp.url = 'http://example.com/start'
    resp.status_code = 302
    resp.headers = {'Location': 'http://example.com/loop'}
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    del resp.raw._original_response

    # Function to generate new responses for the infinite loop
    def send_side_effect(request, **kwargs):
        r = Response()
        r.url = request.url
        r.status_code = 302
        r.headers = {'Location': 'http://example.com/loop'}
        r._content = b""
        r._content_consumed = True
        r.raw = MagicMock()
        del r.raw._original_response
        return r

    with patch.object(Session, 'send', side_effect=send_side_effect):
        with patch('requests.sessions.extract_cookies_to_jar'):
            
            with pytest.raises(TooManyRedirects) as excinfo:
                # Consume generator to trigger loop
                list(session.resolve_redirects(resp, req))
            
            assert "Exceeded 2 redirects" in str(excinfo.value)

'''
Execution failed:

with patch.object(Session, 'send', side_effect=send_side_effect):
            with patch('requests.sessions.extract_cookies_to_jar'):
    
>               with pytest.raises(TooManyRedirects) as excinfo:
E               Failed: DID NOT RAISE <class 'requests.exceptions.TooManyRedirects'>

eval/tests/generated_tests/P1/resolve_redirects/test_P1_resolve_redirects_2.py:39: Failed
'''