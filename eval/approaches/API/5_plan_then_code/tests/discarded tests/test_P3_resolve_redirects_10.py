import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_empty_if_no_redirect():
    """
    Test that resolve_redirects yields nothing if the response is not a redirect.
    """
    session = Session()
    
    req = Request(method="GET", url="http://example.com/ok").prepare()
    
    resp = Response()
    resp.status_code = 200
    # No Location header
    resp.url = "http://example.com/ok"
    resp._content = b"OK"
    resp._content_consumed = True
    resp.request = req
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    
    # Verify generator is empty
    with pytest.raises(StopIteration):
        next(gen)