import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_header_purging_301():
    """
    Test that specific headers (Content-Length, Content-Type, Transfer-Encoding)
    are removed and body is cleared when redirecting with status code 301.
    """
    session = Session()
    
    # Original POST request with body and headers
    req = PreparedRequest()
    req.url = "http://example.com/resource"
    req.method = "POST"
    req.headers = {
        "Content-Length": "100",
        "Content-Type": "application/json",
        "Transfer-Encoding": "chunked",
        "X-Keep-Me": "true"
    }
    req.body = b'{"data": 123}'
    
    # 301 Response
    resp = Response()
    resp.url = "http://example.com/resource"
    resp.status_code = 301
    resp.raw = MagicMock()
    
    # Mock redirect flow
    session.get_redirect_target = MagicMock(side_effect=["http://example.com/new", None])
    session.send = MagicMock(return_value=Response())
    
    # rebuild_method might be called, but we specifically want to test the purging logic
    # which happens inside resolve_redirects explicitly.
    session.rebuild_method = MagicMock() 
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock()
    
    with patch("requests.sessions.extract_cookies_to_jar"):
        list(session.resolve_redirects(resp, req))
        
    # Capture the request sent via session.send
    sent_req = session.send.call_args[0][0]
    
    # Assert headers were purged
    assert "Content-Length" not in sent_req.headers
    assert "Content-Type" not in sent_req.headers
    assert "Transfer-Encoding" not in sent_req.headers
    
    # Assert other headers remain
    assert sent_req.headers["X-Keep-Me"] == "true"
    
    # Assert body is cleared
    assert sent_req.body is None


'''
Execution failed:

with patch("requests.sessions.extract_cookies_to_jar"):
>           list(session.resolve_redirects(resp, req))

eval/tests/generated_tests/P0/resolve_redirects/test_P0_resolve_redirects_3.py:42: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
requests/src/requests/sessions.py:241: in resolve_redirects
    merge_cookies(prepared_request._cookies, self.cookies)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

cookiejar = None, cookies = <RequestsCookieJar[]>

    def merge_cookies(cookiejar, cookies):
        """Add cookies to cookiejar and returns a merged CookieJar.
    
        :param cookiejar: CookieJar object to add the cookies to.
        :param cookies: Dictionary or CookieJar object to be added.
        :rtype: CookieJar
        """
        if not isinstance(cookiejar, cookielib.CookieJar):
>           raise ValueError("You can only merge into CookieJar")
E           ValueError: You can only merge into CookieJar

requests/src/requests/cookies.py:550: ValueError
'''