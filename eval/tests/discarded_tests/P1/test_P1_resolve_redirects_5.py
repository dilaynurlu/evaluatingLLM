import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_resolve_redirects_relative_fragment_handling():
    session = Session()
    
    # Request with fragment
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/path/resource#frag1')
    
    resp = Response()
    resp.url = 'http://example.com/path/resource'
    resp.status_code = 302
    # Relative redirect
    resp.headers = {'Location': '../other'}
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    del resp.raw._original_response

    with patch.object(Session, 'send') as mock_send:
        with patch('requests.sessions.extract_cookies_to_jar'):
            
            # We use yield_requests=True to inspect the resolved URL without caring about the next response
            gen = session.resolve_redirects(resp, req, yield_requests=True)
            new_req = next(gen)
            
            # Expected:
            # 1. Base: http://example.com/path/resource
            # 2. Relative: ../other -> http://example.com/other
            # 3. Fragment: #frag1 (inherited from original request)
            assert new_req.url == 'http://example.com/other#frag1'


'''
Exectuion failed:

 # We use yield_requests=True to inspect the resolved URL without caring about the next response
                gen = session.resolve_redirects(resp, req, yield_requests=True)
>               new_req = next(gen)
                          ^^^^^^^^^
E               StopIteration

eval/tests/generated_tests/P1/resolve_redirects/test_P1_resolve_redirects_5.py:28: StopIteration
'''