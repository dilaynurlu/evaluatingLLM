import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the number of redirects exceeds max_redirects.
    Refined to ensure clean mocking and state isolation.
    """
    session = Session()
    session.max_redirects = 1
    
    # Setup chain: source -> redirect1 -> redirect2 (should fail)
    
    # Second Response (would be the result of the first redirect)
    # This response attempts another redirect
    resp2 = Response()
    resp2.status_code = 302
    resp2.headers = CaseInsensitiveDict({"Location": "/final"})
    resp2.url = "http://example.com/redirect1"
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = MagicMock()
    # We must link the request to the response for the generator to process it correctly if it inspects resp.request
    # However, resolve_redirects constructs the request for the *next* step based on the previous response.
    # When session.send returns resp2, we simulate that.
    
    session.send = MagicMock(return_value=resp2)
    
    # Initial Request
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/source")
    
    # Initial Response (First Redirect)
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers = CaseInsensitiveDict({"Location": "/redirect1"})
    resp1.url = "http://example.com/source"
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    resp1.request = req
    
    gen = session.resolve_redirects(resp1, req)
    
    # First iteration: Should yield resp2 (the result of following /redirect1)
    # Internally, resolve_redirects calls session.send, which returns resp2.
    first_yield = next(gen)
    assert first_yield == resp2
    
    # Second iteration: It sees resp2 is a redirect. It checks max_redirects.
    # We have done 1 redirect. limit is 1. Attempting next one should fail.
    with pytest.raises(TooManyRedirects) as excinfo:
        next(gen)
    
    assert "Exceeded 1 redirects" in str(excinfo.value)