import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_redirects_exceeded():
    """
    Test that TooManyRedirects is raised when the redirect limit is exceeded.
    """
    session = Session()
    session.max_redirects = 1
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/1')
    
    # First response triggers the loop
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = '/2'
    resp1.url = 'http://example.com/1'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()

    # Second response (redirects again)
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers['Location'] = '/3'
    resp2.url = 'http://example.com/2'
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = MagicMock()
    
    # Mock send to return resp2
    session.send = MagicMock(return_value=resp2)
    
    # The generator should yield resp2 (first redirect successful)
    # Then loop again. 'hist' will now have [resp1, resp2].
    # len(hist) is 2. max_redirects is 1. Should raise.
    
    gen = session.resolve_redirects(resp1, req)
    
    # First iteration works
    r = next(gen)
    assert r == resp2
    
    # Second iteration raises
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)