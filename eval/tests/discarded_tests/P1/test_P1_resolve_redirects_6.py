import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_resolve_redirects_schemeless_url():
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='https://secure.example.com/foo')
    
    resp = Response()
    resp.url = 'https://secure.example.com/foo'
    resp.status_code = 302
    # Schemeless redirect (starts with //)
    resp.headers = {'Location': '//cdn.example.com/bar'}
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    del resp.raw._original_response

    with patch.object(Session, 'send') as mock_send:
        with patch('requests.sessions.extract_cookies_to_jar'):
            
            gen = session.resolve_redirects(resp, req, yield_requests=True)
            new_req = next(gen)
            
            # Should inherit scheme 'https' from response URL
            assert new_req.url == 'https://cdn.example.com/bar'


'''
Exectuion failed:

 with patch.object(Session, 'send') as mock_send:
            with patch('requests.sessions.extract_cookies_to_jar'):
    
                gen = session.resolve_redirects(resp, req, yield_requests=True)
>               new_req = next(gen)
                          ^^^^^^^^^
E               StopIteration

eval/tests/generated_tests/P1/resolve_redirects/test_P1_resolve_redirects_6.py:26: StopIteration
'''