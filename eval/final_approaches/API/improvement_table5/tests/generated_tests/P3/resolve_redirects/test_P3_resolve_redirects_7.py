import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest
from unittest.mock import MagicMock

def test_resolve_redirects_yield_requests_mode():
    """
    Test that when yield_requests is True:
    1. The generator yields the PreparedRequest object.
    2. The session.send method is NOT called.
    """
    session = Session()
    
    req = Request("GET", "http://example.com/start").prepare()
    
    resp = Response()
    resp.request = req
    resp.url = "http://example.com/start"
    resp.status_code = 302
    resp.headers["Location"] = "http://example.com/finish"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Ensure send is NOT called
    session.send = MagicMock(side_effect=Exception("Should not send request in yield_requests mode"))
    
    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    yielded_obj = next(gen)
    
    # Assertions
    assert isinstance(yielded_obj, PreparedRequest)
    assert yielded_obj.url == "http://example.com/finish"
    assert yielded_obj.method == "GET"
    
    # Verify that the generator state is handled correctly.
    # In yield_requests mode, the logic essentially prepares the transition and yields it.
    # We verify that we can consume it without side effects.
    session.send.assert_not_called()