import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_fragment_handling():
    """
    Test that resolve_redirects preserves the original URL fragment if the redirect
    URL does not have one, as per RFC 7231 7.1.2.
    """
    session = Session()
    
    # Request with a fragment
    url = "http://example.com/page#section1"
    req = Request(method="GET", url=url).prepare()
    
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/newpage"
    resp.url = url
    resp._content = b""
    resp._content_consumed = True
    resp.request = req
    
    resp_next = Response()
    resp_next.status_code = 200
    resp_next._content = b""
    resp_next._content_consumed = True
    
    session.send = Mock(return_value=resp_next)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Verify
    sent_request = session.send.call_args[0][0]
    # The new URL should inherit the fragment "#section1"
    assert sent_request.url == "http://example.com/newpage#section1"