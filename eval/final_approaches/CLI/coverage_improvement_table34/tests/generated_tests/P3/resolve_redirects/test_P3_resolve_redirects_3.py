import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from requests.status_codes import codes
from unittest.mock import Mock

def test_resolve_redirects_303_to_GET():
    session = requests.Session()
    
    req = PreparedRequest()
    req.url = "http://example.com/post"
    req.method = "POST"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = codes.see_other # 303
    resp.headers = {"location": "http://example.com/get"}
    resp.url = "http://example.com/post"
    resp.request = req
    resp.raw = Mock()
    resp.raw.headers = {}
    resp.history = []
    
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.raw = Mock()
    new_resp.raw.headers = {}
    session.send = Mock(return_value=new_resp)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    args, kwargs = session.send.call_args
    assert args[0].method == "GET"