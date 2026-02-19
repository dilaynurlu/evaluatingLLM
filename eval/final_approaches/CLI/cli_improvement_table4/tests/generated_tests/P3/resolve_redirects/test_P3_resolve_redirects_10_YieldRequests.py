import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_yield_requests():
    session = requests.Session()
    
    req = PreparedRequest()
    req.url = "http://example.com/old"
    req.headers = {}
    req._cookies = RequestsCookieJar()
    req._body_position = None
    
    resp = Mock()
    resp.is_redirect = True
    resp.status_code = 301
    resp.headers = {"location": "http://example.com/new"}
    resp.url = "http://example.com/old"
    resp.request = req
    resp.raw = Mock()
    resp.raw.headers = {}
    resp.history = []
    
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    result = next(gen)
    
    assert isinstance(result, PreparedRequest)
    assert result.url == "http://example.com/new"
