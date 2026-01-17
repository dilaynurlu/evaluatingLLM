import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar

def test_resolve_redirects_cookie_handling():
    """
    Test that cookies are extracted from the response and applied to the next request.
    """
    session = Session()
    # Add a session cookie
    session.cookies.set('session_cookie', 's_val')
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/start')
    
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = '/next'
    resp1.url = 'http://example.com/start'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    # Patch extract_cookies_to_jar to simulate a Set-Cookie in resp1
    # We patch it in requests.sessions where it is imported
    with pytest.MonkeyPatch.context() as m:
        def mock_extract(jar, request, response):
            jar.set('resp_cookie', 'r_val')
            
        m.setattr('requests.sessions.extract_cookies_to_jar', mock_extract)
        
        captured_req = []
        def send_mock(request, **kwargs):
            captured_req.append(request)
            resp = Response()
            resp.status_code = 200
            resp.url = request.url
            resp._content = b""
            resp._content_consumed = True
            resp.raw = MagicMock()
            return resp
            
        session.send = MagicMock(side_effect=send_mock)
        
        list(session.resolve_redirects(resp1, req))
        
        assert len(captured_req) == 1
        sent_req = captured_req[0]
        
        # Check that Cookie header contains both session and response cookies
        cookie_header = sent_req.headers.get('Cookie')
        assert cookie_header is not None
        assert 'session_cookie=s_val' in cookie_header
        assert 'resp_cookie=r_val' in cookie_header