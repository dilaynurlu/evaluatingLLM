import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session's max_redirects limit.
    """
    session = Session()
    session.max_redirects = 1  # Low limit to trigger error quickly
    
    req = Request('GET', 'http://example.com/start').prepare()
    
    # Chain: Start -> Redirect1 (302) -> Redirect2 (302) -> [Should Fail before sending Redirect3 request or on processing Redirect2 result]
    
    # Response 1 (passed as input)
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = 'http://example.com/mid'
    resp1.url = 'http://example.com/start'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = Mock()
    
    # Response 2 (returned by first send)
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers['Location'] = 'http://example.com/end'
    resp2.url = 'http://example.com/mid'
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = Mock()
    
    # Mock send to return resp2
    with patch.object(session, 'send', return_value=resp2):
        gen = session.resolve_redirects(resp1, req)
        
        # First iteration yields resp2. 
        # State: hist=[resp1], len(resp1.history)==0. No error yet.
        result1 = next(gen)
        assert result1 is resp2
        
        # Second iteration attempts to process resp2.
        # State: hist=[resp1, resp2]. resp2.history=[resp2] (from slicing hist[1:] in context of logic). 
        # Actually logic is: hist.append(resp). resp.history = hist[1:].
        # Iter 1: resp=resp1. hist=[resp1]. resp1.hist=[]. Yield resp2.
        # Iter 2: resp=resp2. hist=[resp1, resp2]. resp2.hist=[resp2].
        # len(resp2.history) is 1. max_redirects is 1. 1 >= 1 -> Raise.
        
        with pytest.raises(TooManyRedirects) as excinfo:
            next(gen)
            
        assert "Exceeded 1 redirects" in str(excinfo.value)
        # Ensure the exception contains the response that triggered it
        assert excinfo.value.response is resp2