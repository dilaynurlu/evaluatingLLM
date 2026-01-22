from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_cookies():
    session = Session()
    session.cookies = RequestsCookieJar()
    
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "/new", "Set-Cookie": "foo=bar"})
    resp.url = "http://example.com/old"
    resp.raw = Mock()
    # Mocking raw headers for extract_cookies_to_jar
    # It usually expects an object with 'headers' (httplib.Message or similar)
    # We can just use the same dict or a mock
    resp.raw.stream.return_value = [b""]
    msg = Mock()
    msg.get_all.return_value = ["foo=bar"] # for Set-Cookie
    # Actually requests uses compatibility for headers. 
    # Let's use a simpler approach: mock extract_cookies_to_jar in the session module
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.com/old"
    req.headers = CaseInsensitiveDict({})
    req._cookies = RequestsCookieJar()
    
    session.send = Mock(return_value=Response())
    
    # We need to mock extract_cookies_to_jar call inside resolve_redirects
    # because doing it via resp.raw is brittle without real urllib3 response
    
    # However, if we populate session.cookies manually in the test expectation?
    # No, we want to test that resolve_redirects calls extraction.
    
    # Let's patch requests.sessions.extract_cookies_to_jar
    from unittest.mock import patch
    with patch("requests.sessions.extract_cookies_to_jar") as mock_extract:
        def side_effect(jar, request, response):
            jar.set("foo", "bar")
        mock_extract.side_effect = side_effect
        
        list(session.resolve_redirects(resp, req))
    
    # Cookie should be in session (no, extract_cookies_to_jar puts it in prepared_request._cookies 
    # AND merge_cookies puts it in session.cookies?
    # Code:
    # extract_cookies_to_jar(prepared_request._cookies, req, resp.raw)
    # merge_cookies(prepared_request._cookies, self.cookies)
    # prepared_request.prepare_cookies(prepared_request._cookies)
    
    # Wait, extract_cookies_to_jar extracts from response into jar.
    # The first arg is the jar.
    
    # If we mocked it to set 'foo' in the jar passed to it (prepared_request._cookies),
    # then merge_cookies(prepared_request._cookies, self.cookies) merges FROM cookies TO self.cookies?
    # merge_cookies(to, from) usually.
    # merge_cookies(prepared_request._cookies, self.cookies) -> merge self.cookies INTO prepared_request._cookies
    
    # Ah, resolve_redirects logic:
    # extract_cookies_to_jar(prepared_request._cookies, req, resp.raw)
    # merge_cookies(prepared_request._cookies, self.cookies) 
    
    # So session.cookies is NOT updated here?
    # Yes, typically session cookies are updated in Session.request after the call returns.
    # resolve_redirects manages the cookies for the *next* request in the chain.
    
    # So assert "foo" in new_req._cookies
    
    new_req = session.send.call_args[0][0]
    assert "foo" in new_req._cookies