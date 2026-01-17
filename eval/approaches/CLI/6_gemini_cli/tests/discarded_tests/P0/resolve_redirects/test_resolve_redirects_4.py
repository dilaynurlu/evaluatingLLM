
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock

def test_resolve_redirects_303_see_other():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com"
    req.method = "POST"
    req.headers = {}
    
    resp = MagicMock(spec=Response)
    resp.is_redirect = True
    resp.headers = {"location": "http://example.com/new"}
    resp.status_code = 303
    resp.history = []
    resp.url = "http://example.com"
    resp.request = req
    
    def side_effect(request, **kwargs):
        # 303 MUST change to GET
        assert request.method == "GET"
        r = MagicMock(spec=Response)
        r.is_redirect = False
        r.status_code = 200
        r.url = "http://example.com/new"
        r.history = [resp]
        r.request = request
        return r
        
    session.send = MagicMock(side_effect=side_effect)
    
    list(session.resolve_redirects(resp, req))
