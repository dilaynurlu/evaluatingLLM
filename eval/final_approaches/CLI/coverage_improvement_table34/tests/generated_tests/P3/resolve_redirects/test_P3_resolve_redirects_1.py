import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_simple_301():
    session = requests.Session()
    # We do NOT mock rebuild_method, rebuild_proxies, rebuild_auth to allow them to run and increase coverage.
    
    # Initial request
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.method = "GET"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    # Response 301
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.url = "http://example.com/old"
    resp.request = req
    resp.raw = Mock()
    resp.raw.headers = {}
    resp.history = []
    
    # Mock send to return the new response
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.url = "http://example.com/new"
    new_resp.raw = Mock()
    new_resp.raw.headers = {}
    
    # Mock send method on session
    session.send = Mock(return_value=new_resp)
    
    gen = session.resolve_redirects(resp, req)
    result = next(gen)
    
    assert result == new_resp
    assert session.send.call_count == 1
    args, kwargs = session.send.call_args
    assert args[0].url == "http://example.com/new"