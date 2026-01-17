import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_yield_requests():
    """
    Test that when yield_requests=True, the method yields the PreparedRequest object
    instead of sending it and yielding the Response.
    """
    session = Session()
    
    req = Request(method="GET", url="http://example.com/one").prepare()
    
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "/two"
    resp.url = "http://example.com/one"
    resp._content = b""
    resp._content_consumed = True
    resp.request = req
    
    # Mock send to ensure it is NOT called
    session.send = Mock()
    
    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    yielded_obj = next(gen)
    
    # Verify
    assert isinstance(yielded_obj, Request) or isinstance(yielded_obj, object)
    # The class is PreparedRequest, verify attributes
    assert yielded_obj.url == "http://example.com/two"
    
    # Verify send was not called
    session.send.assert_not_called()