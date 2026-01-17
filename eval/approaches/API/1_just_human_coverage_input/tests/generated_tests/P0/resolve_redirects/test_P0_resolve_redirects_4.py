import pytest
from unittest.mock import Mock
from email.message import Message
from requests import Session, Request, Response
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_extract_cookies():
    """
    Test that cookies set in the redirect response are extracted and added 
    to the subsequent request.
    """
    session = Session()
    # Session must have a cookie jar
    session.cookies = RequestsCookieJar()
    
    req = Request('GET', 'http://example.com/login')
    prep_req = req.prepare()
    
    # Setup response with Set-Cookie header
    resp = Response()
    resp.status_code = 302
    resp.url = 'http://example.com/login'
    resp.headers['Location'] = '/dashboard'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    
    # Mocking the raw response for extract_cookies_to_jar
    # requests uses resp.raw._original_response.msg to get headers for cookies
    headers = Message()
    headers.add_header('Set-Cookie', 'auth_token=secret123; Path=/')
    
    mock_orig_response = Mock()
    mock_orig_response.msg = headers
    
    mock_raw = Mock()
    mock_raw._original_response = mock_orig_response
    resp.raw = mock_raw
    
    # Mock next response
    resp_next = Response()
    resp_next.status_code = 200
    resp_next._content = b"Welcome"
    resp_next._content_consumed = True
    
    session.send = Mock(return_value=resp_next)
    
    # Execute
    gen = session.resolve_redirects(resp, prep_req)
    next(gen)
    
    # Verify the next request contains the cookie
    args, _ = session.send.call_args
    sent_req = args[0]
    
    assert 'Cookie' in sent_req.headers
    assert 'auth_token=secret123' in sent_req.headers['Cookie']