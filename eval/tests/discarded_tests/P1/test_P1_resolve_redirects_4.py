import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_resolve_redirects_strip_headers_on_303():
    session = Session()
    
    # Original POST request with body and headers
    req = PreparedRequest()
    req.prepare(
        method='POST',
        url='http://example.com/post',
        headers={
            'Content-Type': 'application/json',
            'Content-Length': '15',
            'Transfer-Encoding': 'chunked',
            'X-Custom': 'KeepMe'
        },
        data='{"key": "val"}'
    )
    
    resp = Response()
    resp.url = 'http://example.com/post'
    resp.status_code = 303  # See Other -> transforms to GET and strips body
    resp.headers = {'Location': 'http://example.com/get'}
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    del resp.raw._original_response

    # Dummy response for send
    resp_next = Response()
    resp_next.status_code = 200
    resp_next._content = b""
    resp_next._content_consumed = True
    resp_next.raw = MagicMock()
    del resp_next.raw._original_response

    with patch.object(Session, 'send', return_value=resp_next) as mock_send:
        with patch('requests.sessions.extract_cookies_to_jar'):
            
            list(session.resolve_redirects(resp, req))
            
            mock_send.assert_called_once()
            sent_req = mock_send.call_args[0][0]
            
            # Method should be changed to GET (handled by rebuild_method inside resolve_redirects)
            assert sent_req.method == 'GET'
            
            # Headers should be stripped
            assert 'Content-Type' not in sent_req.headers
            assert 'Content-Length' not in sent_req.headers
            assert 'Transfer-Encoding' not in sent_req.headers
            # Custom header should remain
            assert sent_req.headers['X-Custom'] == 'KeepMe'
            # Body should be None
            assert sent_req.body is None


'''
Assertion failed:


with patch.object(Session, 'send', return_value=resp_next) as mock_send:
            with patch('requests.sessions.extract_cookies_to_jar'):
    
                list(session.resolve_redirects(resp, req))
    
>               mock_send.assert_called_once()

eval/tests/generated_tests/P1/resolve_redirects/test_P1_resolve_redirects_4.py:45: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <MagicMock name='send' id='281472945884816'>

    def assert_called_once(self):
        """assert that the mock was called only once.
        """
        if not self.call_count == 1:
            msg = ("Expected '%s' to have been called once. Called %s times.%s"
                   % (self._mock_name or 'mock',
                      self.call_count,
                      self._calls_repr()))
>           raise AssertionError(msg)
E           AssertionError: Expected 'send' to have been called once. Called 0 times.

/usr/local/lib/python3.11/unittest/mock.py:918: AssertionError
''' 