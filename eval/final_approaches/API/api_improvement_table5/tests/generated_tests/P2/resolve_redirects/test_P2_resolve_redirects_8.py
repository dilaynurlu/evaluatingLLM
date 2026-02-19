import pytest
from unittest.mock import Mock, patch
import requests
import io

def test_resolve_redirects_rewinds_body():
    """
    Test that the request body is rewound if a redirect occurs and the body is seekable.
    """
    session = requests.Session()
    
    # Create a seekable file-like body
    body_content = b"seekable_data"
    body = io.BytesIO(body_content)
    
    # Prepare request
    # Note: requests.Request(...).prepare() usually sets Content-Length and handles file objects
    req = requests.Request('POST', 'http://example.com/upload', data=body).prepare()
    
    # Explicitly ensure conditions for rewindable logic are met in case prepare() varied
    if 'Content-Length' not in req.headers:
        req.headers['Content-Length'] = str(len(body_content))
    # We must ensure _body_position is set to valid start
    if req._body_position is None:
        req._body_position = 0
    
    # Simulate partial read of the body before the redirect logic runs
    body.seek(5)
    
    initial_resp = requests.Response()
    initial_resp.status_code = 307 # Preserve POST to ensure body is reused
    initial_resp.headers['Location'] = '/retry'
    initial_resp.url = 'http://example.com/upload'
    initial_resp.request = req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    def send_side_effect(request, **kwargs):
        # Check that body was rewound to 0
        current_pos = request.body.tell()
        assert current_pos == 0
        assert request.body.read() == body_content
        
        resp = requests.Response()
        resp.status_code = 200
        resp.url = request.url
        resp.request = request
        resp._content = b''
        resp._content_consumed = True
        resp.raw = Mock()
        return resp

    with patch.object(session, 'send', side_effect=send_side_effect):
        gen = session.resolve_redirects(initial_resp, req)
        next(gen)