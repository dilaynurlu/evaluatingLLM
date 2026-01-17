import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_too_many_redirects():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session.max_redirects limit.
    """
    session = Session()
    session.max_redirects = 2
    
    initial_url = 'http://example.com/loop'
    req = Request('GET', initial_url).prepare()
    
    # Prepare a response that redirects to itself
    resp = Response()
    resp.status_code = 302
    resp.url = initial_url
    resp.headers['Location'] = initial_url
    resp._content = b''
    resp._content_consumed = True
    resp.request = req
    
    # Mock send to always return the same redirect response
    # We must return a new Response object each time to simulate a real loop
    # and ensure history handling doesn't crash on identical objects
    def side_effect(request, **kwargs):
        r = Response()
        r.status_code = 302
        r.url = request.url
        r.headers['Location'] = request.url
        r._content = b''
        r._content_consumed = True
        r.request = request
        return r
        
    session.send = Mock(side_effect=side_effect)
    
    gen = session.resolve_redirects(resp, req)
    
    with pytest.raises(TooManyRedirects) as excinfo:
        # Consume the generator until it raises
        for _ in gen:
            pass
            
    assert "Exceeded 2 redirects" in str(excinfo.value)