import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_relative():
    session = requests.Session()
    
    req = PreparedRequest()
    req.url = "http://example.com/path/old"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "../new"} # Relative
    resp.url = "http://example.com/path/old"
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
    # http://example.com/path/old + ../new -> http://example.com/new
    assert args[0].url == "http://example.com/new"