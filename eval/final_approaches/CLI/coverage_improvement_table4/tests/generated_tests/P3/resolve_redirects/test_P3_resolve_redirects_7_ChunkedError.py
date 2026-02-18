import pytest
import requests
from requests.models import PreparedRequest, Response
from requests.exceptions import ChunkedEncodingError
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_resolve_redirects_chunked_error():
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
    
    # Mock content access raising ChunkedEncodingError
    type(resp).content = property(lambda self: (_ for _ in ()).throw(ChunkedEncodingError))
    
    # Mock send
    new_resp = Mock()
    new_resp.is_redirect = False
    new_resp.raw = Mock()
    new_resp.raw.headers = {}
    session.send = Mock(return_value=new_resp)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Verify resp.raw.read(decode_content=False) was called
    resp.raw.read.assert_called_with(decode_content=False)
