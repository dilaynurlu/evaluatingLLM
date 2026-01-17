import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_too_many_redirects_and_history():
    """
    Test that TooManyRedirects is raised when the number of redirects
    exceeds the session's max_redirects limit, and that response history
    is correctly populated.
    """
    session = Session()
    session.max_redirects = 1
    
    # Initial request
    url = "http://example.com/start"
    req = Request(method="GET", url=url).prepare()
    
    # First Response (Redirect 1)
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers["Location"] = "/step1"
    resp1.url = url
    resp1._content = b""
    resp1._content_consumed = True
    resp1.request = req
    
    # Second Response (Redirect 2)
    resp2 = Response()
    resp2.status_code = 301
    resp2.headers["Location"] = "/step2"
    resp2.url = "http://example.com/step1"
    resp2._content = b""
    resp2._content_consumed = True
    # In a real flow, resp2.request is the request that generated resp2
    # We rely on the generator to yield resp2 after setting its history
    
    # Mock send to return resp2
    session.send = Mock(return_value=resp2)
    
    # Execute
    gen = session.resolve_redirects(resp1, req)
    
    # The first yield is the response from the first redirect (resp2)
    first_redirect_response = next(gen)
    
    # Verify resp2 is returned
    assert first_redirect_response == resp2
    
    # Verify history was populated on the yielded response
    # It should contain the previous response (resp1)
    assert len(first_redirect_response.history) == 1
    assert first_redirect_response.history[0] == resp1
    
    # The next iteration attempts to follow resp2's redirect.
    # History would grow to [resp1, resp2] (len 2), which > max_redirects (1).
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)