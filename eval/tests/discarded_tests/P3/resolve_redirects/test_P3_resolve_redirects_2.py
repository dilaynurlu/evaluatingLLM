import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_redirects_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session.max_redirects limit.
    """
    session = Session()
    session.max_redirects = 1
    
    req = Request('GET', 'http://example.com/step1')
    prep_req = session.prepare_request(req)
    
    # First response (301)
    resp1 = Response()
    resp1.status_code = 301
    resp1.url = 'http://example.com/step1'
    resp1.headers['Location'] = 'http://example.com/step2'
    resp1.request = prep_req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    # Second response (301)
    resp2 = Response()
    resp2.status_code = 301
    resp2.url = 'http://example.com/step2'
    resp2.headers['Location'] = 'http://example.com/step3'
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = MagicMock()
    
    # Third response (200) - should not be reached due to exception
    resp3 = Response()
    resp3.status_code = 200
    
    # session.send should return resp2 first
    session.send = MagicMock(return_value=resp2)
    
    gen = session.resolve_redirects(resp1, prep_req)
    
    # The first iteration should succeed and yield resp2
    assert next(gen) is resp2
    
    # The second iteration attempts another redirect but should detect loop limit
    # History at this point will contain [resp1, resp2] (len 2)
    # max_redirects is 1, so 2 > 1 -> Exception
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
        
    assert "Exceeded 1 redirects" in str(excinfo.value)
    # Verify connections released
    resp1.raw.release_conn.assert_called()
    resp2.raw.release_conn.assert_called()