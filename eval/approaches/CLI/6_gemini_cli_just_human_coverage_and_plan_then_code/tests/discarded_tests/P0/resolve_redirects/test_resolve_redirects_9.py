
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock

def test_resolve_redirects_cookie_handling():
    session = Session()
    session.cookies = RequestsCookieJar()
    
    req = PreparedRequest()
    req.url = "http://example.com/foo"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    
    resp = MagicMock(spec=Response)
    resp.is_redirect = True
    resp.headers = {"location": "http://example.com/bar", "Set-Cookie": "foo=bar"}
    resp.status_code = 301
    resp.history = []
    resp.url = "http://example.com/foo"
    resp.request = req
    resp.raw = MagicMock()
    # Mocking extract_cookies_to_jar behavior essentially
    
    def side_effect(request, **kwargs):
        # In real execution, extract_cookies_to_jar would populate the jar
        # But we are testing resolve_redirects logic flow
        r = MagicMock(spec=Response)
        r.is_redirect = False
        r.status_code = 200
        r.url = "http://example.com/bar"
        r.history = [resp]
        r.request = request
        return r
        
    session.send = MagicMock(side_effect=side_effect)
    
    list(session.resolve_redirects(resp, req))
