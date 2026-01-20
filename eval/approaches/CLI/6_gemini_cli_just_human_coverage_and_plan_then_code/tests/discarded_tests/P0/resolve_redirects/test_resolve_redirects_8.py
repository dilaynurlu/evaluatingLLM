
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock

def test_resolve_redirects_fragment_handling():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com/foo#frag"
    req.method = "GET"
    req.headers = {}
    
    resp = MagicMock(spec=Response)
    resp.is_redirect = True
    resp.headers = {"location": "http://example.com/bar"}
    resp.status_code = 301
    resp.history = []
    resp.url = "http://example.com/foo"
    resp.request = req
    
    def side_effect(request, **kwargs):
        # Should persist fragment
        assert request.url == "http://example.com/bar#frag"
        r = MagicMock(spec=Response)
        r.is_redirect = False
        r.status_code = 200
        r.url = "http://example.com/bar#frag"
        r.history = [resp]
        r.request = request
        return r
        
    session.send = MagicMock(side_effect=side_effect)
    
    list(session.resolve_redirects(resp, req))
