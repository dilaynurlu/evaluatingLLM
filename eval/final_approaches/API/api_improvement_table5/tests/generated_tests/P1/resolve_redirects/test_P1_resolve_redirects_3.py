import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_enforces_max_redirects():
    """
    Test that TooManyRedirects is raised when the number of redirects exceeds session.max_redirects.
    """
    session = Session()
    session.max_redirects = 2
    session.send = Mock()

    # Initial Request
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/start')

    # Chain of redirects: start -> step1 -> step2 -> step3 (fail)
    
    # 1. Initial response (start -> step1)
    resp1 = Response()
    resp1.status_code = 302
    resp1.url = 'http://example.com/start'
    resp1.headers['Location'] = 'http://example.com/step1'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True

    # 2. Second response (step1 -> step2)
    resp2 = Response()
    resp2.status_code = 302
    resp2.url = 'http://example.com/step1'
    resp2.headers['Location'] = 'http://example.com/step2'
    resp2._content = b""
    resp2._content_consumed = True

    # 3. Third response (step2 -> step3)
    resp3 = Response()
    resp3.status_code = 302
    resp3.url = 'http://example.com/step2'
    resp3.headers['Location'] = 'http://example.com/step3'
    resp3._content = b""
    resp3._content_consumed = True

    # Configure session.send to return the subsequent responses in order
    session.send.side_effect = [resp2, resp3]

    # Execute and expect error
    gen = session.resolve_redirects(resp1, req)
    
    with pytest.raises(TooManyRedirects) as excinfo:
        list(gen)
    
    assert "Exceeded 2 redirects" in str(excinfo.value)
    
    # Verify execution flow
    # It should have processed resp1 (hist len 0->1), called send for resp2.
    # Processed resp2 (hist len 1->2).
    # Called send for resp3.
    # Processed resp3 (hist len 2->3).
    # 3 > 2 (max_redirects is checked against len(resp.history)).
    # Note: Logic checks `if len(resp.history) >= self.max_redirects`.
    # Depending on implementation details, it might raise at different points, but it must raise.