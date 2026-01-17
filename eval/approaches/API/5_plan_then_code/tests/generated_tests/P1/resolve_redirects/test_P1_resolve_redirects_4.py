import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_relative_location():
    """
    Test that relative URLs in the Location header are correctly resolved
    against the response URL.
    """
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/path/resource")
    
    # 302 Response with relative location
    resp = Response()
    resp.status_code = 302
    # Relative path up one level
    resp.headers["Location"] = "../new_resource"
    resp.url = "http://example.com/path/resource"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    resp_200 = Response()
    resp_200.status_code = 200
    resp_200.url = "http://example.com/new_resource"
    resp_200._content = b""
    resp_200._content_consumed = True
    
    session.send = Mock(return_value=resp_200)
    
    # Execute
    list(session.resolve_redirects(resp, req))
    
    # Verify URL resolution
    # http://example.com/path/resource + ../new_resource -> http://example.com/new_resource
    sent_req = session.send.call_args[0][0]
    assert sent_req.url == "http://example.com/new_resource"