import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_fragment_preservation():
    """
    Test that the URL fragment is preserved from the original request
    if the redirect location does not specify one.
    """
    session = Session()
    
    # Original URL with fragment
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/page#section1")
    
    resp = Response()
    resp.status_code = 302
    # Redirect location without fragment
    resp.headers["Location"] = "http://example.com/other"
    resp.url = "http://example.com/page"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    resp_200 = Response()
    resp_200.status_code = 200
    resp_200.url = "http://example.com/other"
    resp_200._content = b""
    resp_200._content_consumed = True
    
    session.send = Mock(return_value=resp_200)
    
    # Execute
    list(session.resolve_redirects(resp, req))
    
    # Verify the new request has the fragment appended
    sent_req = session.send.call_args[0][0]
    assert sent_req.url == "http://example.com/other#section1"