import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import MagicMock

def test_resolve_redirects_fragment_inheritance():
    """
    Test that the URL fragment is inherited from the original request if the redirect URL
    does not specify one.
    """
    session = Session()
    
    # Request with a fragment
    req = Request("GET", "http://example.com/doc#chapter1").prepare()
    
    # Redirect response to a URL without a fragment
    resp = Response()
    resp.request = req
    resp.url = "http://example.com/doc"
    resp.status_code = 302
    resp.headers["Location"] = "/login"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=Response())
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    sent_req = session.send.call_args[0][0]
    
    # The new URL should maintain the #chapter1 fragment
    assert sent_req.url == "http://example.com/login#chapter1"
    
    # Part 2: Redirect HAS a fragment -> it should take precedence
    session.send.reset_mock()
    req2 = Request("GET", "http://example.com/doc#old").prepare()
    resp.request = req2
    resp.headers["Location"] = "/new#newfrag"
    
    gen2 = session.resolve_redirects(resp, req2)
    next(gen2)
    
    sent_req2 = session.send.call_args[0][0]
    assert sent_req2.url == "http://example.com/new#newfrag"