import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_strip_headers():
    session = requests.Session()
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.headers = {
        "Content-Length": "100",
        "Content-Type": "application/json",
        "Transfer-Encoding": "chunked",
        "Cookie": "foo=bar",
        "X-Custom": "keep"
    }
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 303
    resp.headers = {"location": "http://example.com/new"}
    resp.url = "http://example.com/old"
    resp.request = req
    resp.raw = Mock()
    resp.raw.headers = {}
    resp.history = []
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.headers = {}
    new_resp.raw = Mock()
    new_resp.raw.headers = {}
    session.send = Mock(return_value=new_resp)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    args, kwargs = session.send.call_args
    new_headers = args[0].headers
    assert "Content-Length" not in new_headers
    assert "Content-Type" not in new_headers
    assert "Transfer-Encoding" not in new_headers
    assert "Cookie" not in new_headers
    assert "X-Custom" in new_headers