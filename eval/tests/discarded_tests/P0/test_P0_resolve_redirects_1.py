import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_basic_flow():
    """
    Test a standard 302 redirect scenario.
    Verifies that the function yields the response from the redirect target
    and calls send() with the correct URL.
    """
    session = Session()
    
    # Setup original request and response
    req = PreparedRequest()
    req.url = "http://example.com/start"
    req.headers = {"User-Agent": "test"}
    
    resp_start = Response()
    resp_start.url = "http://example.com/start"
    resp_start.status_code = 302
    resp_start.headers = {"Location": "http://example.com/end"}
    resp_start.raw = MagicMock()  # For content consumption
    
    # Setup response for the redirect
    resp_end = Response()
    resp_end.url = "http://example.com/end"
    resp_end.status_code = 200
    resp_end.raw = MagicMock()
    
    # Mock session methods
    # First call returns target, second call returns None to stop loop
    session.get_redirect_target = MagicMock(side_effect=["http://example.com/end", None])
    session.send = MagicMock(return_value=resp_end)
    session.rebuild_method = MagicMock()
    session.rebuild_auth = MagicMock()
    session.rebuild_proxies = MagicMock(return_value=None)
    
    # Mock extract_cookies_to_jar to avoid complex cookie logic dependencies
    with patch("requests.sessions.extract_cookies_to_jar"):
        gen = session.resolve_redirects(resp_start, req)
        results = list(gen)
    
    # Assertions
    assert len(results) == 1
    assert results[0] == resp_end
    
    # Verify send was called with the redirect URL
    session.send.assert_called_once()
    sent_req = session.send.call_args[0][0]
    assert sent_req.url == "http://example.com/end"
    assert sent_req.headers["User-Agent"] == "test"

'''
Exectuion failed:

 results = list(gen)
                      ^^^^^^^^^

eval/tests/generated_tests/P0/resolve_redirects/test_P0_resolve_redirects_1.py:42: 
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