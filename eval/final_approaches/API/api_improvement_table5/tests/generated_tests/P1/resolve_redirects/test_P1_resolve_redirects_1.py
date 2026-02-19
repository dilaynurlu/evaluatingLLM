import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_301_changes_post_to_get():
    """
    Test that a 301 Moved Permanently redirect converts a POST request to a GET request
    and removes body-related headers (Content-Length, Content-Type).
    """
    session = Session()
    # Mock send to prevent actual network I/O and return the final response
    session.send = Mock()

    # Create the initial POST request
    req = PreparedRequest()
    req.prepare(
        method='POST',
        url='http://example.com/source',
        data='some_data',
        headers={'Content-Type': 'text/plain'}
    )
    # Sanity check: Content-Length should be present
    assert 'Content-Length' in req.headers

    # Create the initial 301 Response
    resp = Response()
    resp.status_code = 301
    resp.url = 'http://example.com/source'
    resp.headers['Location'] = 'http://example.com/dest'
    resp.request = req
    # Pre-consume content to avoid raw socket access
    resp._content = b""
    resp._content_consumed = True

    # Setup the response that session.send will return for the redirect
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = 'http://example.com/dest'
    final_resp._content = b"success"
    final_resp._content_consumed = True
    session.send.return_value = final_resp

    # Execute resolve_redirects
    # It returns a generator, so we convert to list to consume it
    history = list(session.resolve_redirects(resp, req))

    # Verification
    assert len(history) == 1
    assert history[0] is final_resp

    # Verify the request that was sent
    assert session.send.call_count == 1
    sent_req = session.send.call_args[0][0]

    # RFC 7231: 301/302 redirects for POST convert to GET
    assert sent_req.method == 'GET'
    assert sent_req.url == 'http://example.com/dest'
    assert sent_req.body is None
    
    # Body headers should be purged
    assert 'Content-Length' not in sent_req.headers
    assert 'Content-Type' not in sent_req.headers