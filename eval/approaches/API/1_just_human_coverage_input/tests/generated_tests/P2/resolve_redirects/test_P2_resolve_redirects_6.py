import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar, create_cookie

def test_resolve_redirects_extract_cookies_to_next_request():
    """
    Test that cookies sent in the redirect response (Set-Cookie) are extracted
    and included in the subsequent request's headers.
    """
    session = Session()
    # Ensure session has a cookie jar
    session.cookies = RequestsCookieJar()
    
    req = Request('GET', 'http://example.com/login').prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.url = 'http://example.com/login'
    resp.headers = CaseInsensitiveDict({'Location': 'http://example.com/dashboard'})
    resp.raw = MagicMock()
    
    final_resp = Response()
    final_resp.status_code = 200
    session.send = Mock(return_value=final_resp)
    
    # Patch extract_cookies_to_jar in the requests.sessions module
    # to simulate cookie extraction without needing valid raw HTTP headers/mocking urllib3.
    with pytest.MonkeyPatch().context() as mp:
        mock_extract = Mock()
        def side_effect(jar, request, response):
            # Simulate receiving a cookie from the response
            jar.set_cookie(create_cookie('session_id', 'secret123'))
        
        mock_extract.side_effect = side_effect
        mp.setattr('requests.sessions.extract_cookies_to_jar', mock_extract)
        
        gen = session.resolve_redirects(resp, req)
        next(gen)
        
        called_req = session.send.call_args[0][0]
        
        # Check if the extracted cookie was added to the new request headers
        assert 'Cookie' in called_req.headers
        assert 'session_id=secret123' in called_req.headers['Cookie']