import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_loop_detection():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session's max_redirects limit.
    """
    session = requests.Session()
    session.max_redirects = 2
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/1')
    
    # Setup a chain of redirects
    # Initial response
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = 'http://example.com/2'
    resp1.url = 'http://example.com/1'
    resp1.request = req
    resp1._content = b''
    
    # Second response (first redirect outcome)
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers['Location'] = 'http://example.com/3'
    resp2.url = 'http://example.com/2'
    resp2._content = b''

    # Third response (second redirect outcome)
    resp3 = Response()
    resp3.status_code = 302
    resp3.headers['Location'] = 'http://example.com/4'
    resp3.url = 'http://example.com/3'
    resp3._content = b''
    
    # Mock send to return the sequence of responses
    with patch.object(session, 'send', side_effect=[resp2, resp3]) as mock_send:
        gen = session.resolve_redirects(resp1, req)
        
        # First redirect (1 -> 2)
        r2 = next(gen)
        assert r2.url == 'http://example.com/2'
        
        # Second redirect (2 -> 3)
        r3 = next(gen)
        assert r3.url == 'http://example.com/3'
        
        # Third redirect attempts to go to 4, but max_redirects=2
        # On the next iteration, history length checks will trigger exception
        with pytest.raises(TooManyRedirects) as excinfo:
            next(gen)
            
        assert "Exceeded 2 redirects" in str(excinfo.value)