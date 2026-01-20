
import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from unittest.mock import MagicMock

def test_resolve_redirects_no_location():
    session = Session()
    req = PreparedRequest()
    req.url = "http://example.com"
    req.method = "GET"
    req.headers = {}
    
    resp = MagicMock(spec=Response)
    resp.is_redirect = True
    # Missing location header
    resp.headers = {}
    resp.status_code = 301
    resp.history = []
    resp.url = "http://example.com"
    resp.request = req
    
    # Should yield nothing if get_redirect_target returns None
    gen = session.resolve_redirects(resp, req)
    assert list(gen) == []
