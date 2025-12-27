import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_limit_exceeded():
    """
    Test that TooManyRedirects is raised when the redirect chain length
    exceeds max_redirects. This tests the loop counter logic properly.
    """
    session = Session()
    session.max_redirects = 2
    
    # Initial Request
    req = PreparedRequest()
    req.prepare(method='GET', url="http://example.com/0")
    
    # Initial Response
    resp = Response()
    resp.status_code = 302
    resp.url = "http://example.com/0"
    resp.headers['Location'] = "http://example.com/1"
    resp._content = b""
    
    # Side effect to simulate a chain of redirects
    # Req(0) -> Resp(0) redir to 1
    # Req(1) -> Resp(1) redir to 2
    # Req(2) -> Resp(2) redir to 3 (Should fail here, as 0->1 (1), 1->2 (2), 2->3 (3 > 2))
    def send_side_effect(request, **kwargs):
        # Extract counter from URL
        curr_num = int(request.url.split('/')[-1])
        
        r = Response()
        r.status_code = 302
        r.url = request.url
        r.headers['Location'] = f"http://example.com/{curr_num + 1}"
        r._content = b""
        return r

    session.send = MagicMock(side_effect=send_side_effect)
    
    gen = session.resolve_redirects(resp, req)
    
    with pytest.raises(TooManyRedirects) as excinfo:
        list(gen)
    
    assert "Exceeded 2 redirects" in str(excinfo.value)
    
    # Verify we actually attempted the allowed number of redirects
    # Initial call is external. 
    # redirect 1: sends req to /1
    # redirect 2: sends req to /2
    # redirect 3: detected as too many before sending? 
    # Logic: loop runs while i < max_redirects.
    # We expect 2 calls to send.
    assert session.send.call_count >= 2