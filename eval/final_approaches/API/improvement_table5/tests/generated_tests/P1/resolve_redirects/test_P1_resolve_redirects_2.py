import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_307_preserves_post_method():
    """
    Test that a 307 Temporary Redirect preserves the POST method and the request body.
    """
    session = Session()
    session.send = Mock()

    # Create the initial POST request with body
    req = PreparedRequest()
    req.prepare(
        method='POST',
        url='http://example.com/api/v1',
        data=b'payload_data',
        headers={'Content-Type': 'application/octet-stream'}
    )

    # Create the initial 307 Response
    resp = Response()
    resp.status_code = 307
    resp.url = 'http://example.com/api/v1'
    resp.headers['Location'] = 'http://example.com/api/v2'
    resp.request = req
    resp._content = b""
    resp._content_consumed = True

    # Setup the final response
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = 'http://example.com/api/v2'
    final_resp._content = b"ok"
    final_resp._content_consumed = True
    session.send.return_value = final_resp

    # Execute
    history = list(session.resolve_redirects(resp, req))

    # Verify
    assert len(history) == 1
    assert history[0] is final_resp

    assert session.send.call_count == 1
    sent_req = session.send.call_args[0][0]

    # 307 must preserve method and body
    assert sent_req.method == 'POST'
    assert sent_req.url == 'http://example.com/api/v2'
    assert sent_req.body == b'payload_data'
    assert sent_req.headers['Content-Type'] == 'application/octet-stream'
    assert 'Content-Length' in sent_req.headers