import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_simple_301_behavior():
    """
    Test a simple 301 Redirect scenario with Relative URL resolution.
    
    Improvements based on critique:
    1. Tests Relative URL resolution (Location: /relative) to ensure it is joined correctly.
    2. Verifies that the connection of the consumed response is released (resp.raw.release_conn).
    """
    session = Session()
    
    # Setup initial request
    req = Request('GET', 'http://example.com/original')
    prep_req = session.prepare_request(req)
    
    # Setup initial response triggering the redirect
    resp = Response()
    resp.status_code = 301
    resp.url = 'http://example.com/original'
    # Use a relative URL to test resolution logic
    resp.headers['Location'] = '/relative/redirect' 
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    
    # Mock raw response to verify connection release
    resp.raw = MagicMock()

    # Setup the response for the redirected request
    resp_final = Response()
    resp_final.status_code = 200
    resp_final.url = 'http://example.com/relative/redirect'
    resp_final.request = None 
    resp_final._content = b"OK"
    resp_final._content_consumed = True
    resp_final.raw = MagicMock()

    # Mock session.send to return the final response
    session.send = MagicMock(return_value=resp_final)

    # Execute the generator
    gen = session.resolve_redirects(resp, prep_req)
    history = list(gen)

    # Verifications
    assert len(history) == 1
    assert history[0] is resp_final
    
    # Verify relative URL was resolved to absolute
    assert session.send.call_count == 1
    args, kwargs = session.send.call_args
    sent_request = args[0]
    
    assert sent_request.url == 'http://example.com/relative/redirect'
    assert sent_request.method == 'GET'
    
    # Verify that the previous connection was released
    resp.raw.release_conn.assert_called_once()