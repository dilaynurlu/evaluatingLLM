import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_enforces_max_redirects():
    """
    Test that resolve_redirects raises TooManyRedirects when the 
    number of redirects exceeds session.max_redirects.
    """
    session = Session()
    session.max_redirects = 1
    
    req = Request('GET', 'http://example.com/1').prepare()
    
    # First response (302)
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = 'http://example.com/2'
    resp1.url = 'http://example.com/1'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    
    # Second response (302) - returned by send()
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers['Location'] = 'http://example.com/3'
    resp2.url = 'http://example.com/2'
    resp2.request = req.copy()
    resp2.request.url = 'http://example.com/2'
    resp2._content = b""
    resp2._content_consumed = True
    
    # Mock send to return resp2, then a third response if called again
    resp3 = Response()
    resp3.status_code = 200
    session.send = Mock(side_effect=[resp2, resp3])
    
    gen = session.resolve_redirects(resp1, req)
    
    # First iteration should succeed (1 redirect allowed)
    # The generator yields the result of the first redirect (resp2)
    result1 = next(gen)
    assert result1.url == 'http://example.com/2'
    
    # Second iteration should fail because max_redirects is 1
    # We are now attempting the 2nd redirect (from 2 to 3)
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)