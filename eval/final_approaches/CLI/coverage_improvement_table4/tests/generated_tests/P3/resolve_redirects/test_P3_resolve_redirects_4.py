import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from requests.status_codes import codes
from unittest.mock import Mock

def test_resolve_redirects_307_preserve_POST():
    session = requests.Session()
    
    req = PreparedRequest()
    req.url = "http://example.com/post"
    req.method = "POST"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None # Not rewindable for this test, but 307 usually requires it.
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = codes.temporary_redirect # 307
    resp.headers = {"location": "http://example.com/post2"}
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
    assert args[0].method == "POST"