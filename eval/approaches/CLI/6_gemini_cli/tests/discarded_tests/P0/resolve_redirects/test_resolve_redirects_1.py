
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.exceptions import TooManyRedirects
from unittest.mock import MagicMock

def test_resolve_redirects_too_many():
    session = Session()
    session.max_redirects = 1
    
    req = PreparedRequest()
    req.url = "http://example.com"
    req.headers = {}
    
    resp = MagicMock(spec=Response)
    resp.is_redirect = True
    resp.headers = {"location": "http://example.com/1"}
    resp.status_code = 301
    resp.history = []
    resp.url = "http://example.com"
    resp.request = req
    
    # We need to mock send to return another redirect response
    def side_effect(*args, **kwargs):
        r = MagicMock(spec=Response)
        r.is_redirect = True
        r.headers = {"location": "http://example.com/2"}
        r.status_code = 301
        r.url = "http://example.com/1"
        r.history = [resp]
        r.request = args[0]
        return r
        
    session.send = MagicMock(side_effect=side_effect)
    
    gen = session.resolve_redirects(resp, req)
    
    with pytest.raises(TooManyRedirects):
        list(gen)
