import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_yield_requests_mode():
    """
    Test that when yield_requests=True, the generator yields the PreparedRequest object
    for the redirect instead of sending it and yielding the response.
    """
    session = Session()
    session.send = Mock()

    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/page')

    resp = Response()
    resp.status_code = 302
    resp.url = 'http://example.com/page'
    resp.headers['Location'] = 'http://example.com/login'
    resp.request = req
    resp._content = b""
    resp._content_consumed = True

    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    results = list(gen)

    # Should yield exactly one item which is the prepared request
    assert len(results) == 1
    yielded_req = results[0]
    
    assert isinstance(yielded_req, PreparedRequest)
    assert yielded_req.url == 'http://example.com/login'
    assert yielded_req.method == 'GET'

    # Important: session.send should NOT be called in this mode
    assert session.send.call_count == 0