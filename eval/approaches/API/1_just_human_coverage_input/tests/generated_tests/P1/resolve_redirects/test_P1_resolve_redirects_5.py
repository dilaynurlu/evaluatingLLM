import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response

def test_resolve_redirects_fragment_inheritance():
    """
    Test that if a redirect location has no fragment, the fragment from the 
    original URL is preserved in the new request URL (RFC 7231).
    """
    session = Session()
    
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = "http://example.com/target#original-frag"
    final_resp._content = b"ok"
    final_resp._content_consumed = True
    session.send = Mock(return_value=final_resp)

    # Request with fragment
    req = Request("GET", "http://example.com/source#original-frag").prepare()
    
    # Response redirecting to a URL without fragment
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "/target"
    resp.url = "http://example.com/source"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()

    # Run
    gen = session.resolve_redirects(resp, req)
    next(gen)

    # Check sent request
    sent_req = session.send.call_args[0][0]
    
    # The new URL should be resolved relative to source AND inherit fragment
    assert sent_req.url == "http://example.com/target#original-frag"