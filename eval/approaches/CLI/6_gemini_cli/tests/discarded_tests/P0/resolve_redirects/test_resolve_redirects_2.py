
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock

def test_resolve_redirects_301():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com"
    req.method = "GET"
    req.headers = {}
    
    resp = MagicMock(spec=Response)
    resp.is_redirect = True
    resp.headers = {"location": "http://example.com/new"}
    resp.status_code = 301
    resp.history = []
    resp.url = "http://example.com"
    resp.request = req
    
    def side_effect(*args, **kwargs):
        r = MagicMock(spec=Response)
        r.is_redirect = False
        r.status_code = 200
        r.url = "http://example.com/new"
        r.history = [resp]
        r.request = args[0]
        return r
        
    session.send = MagicMock(side_effect=side_effect)
    
    gen = session.resolve_redirects(resp, req)
    redirects = list(gen)
    
    assert len(redirects) == 1
    assert redirects[0].status_code == 200
    assert redirects[0].url == "http://example.com/new"
