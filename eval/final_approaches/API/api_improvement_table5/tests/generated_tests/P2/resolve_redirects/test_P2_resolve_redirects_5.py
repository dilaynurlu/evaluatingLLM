import pytest
from unittest.mock import Mock, patch
import requests
from requests.exceptions import ChunkedEncodingError

def test_resolve_redirects_content_consumption_error():
    """
    Test that if accessing resp.content raises a ChunkedEncodingError, 
    the function falls back to reading raw socket with decode_content=False.
    """
    session = requests.Session()
    
    initial_req = requests.Request('GET', 'http://example.com/bad-chunk').prepare()
    
    initial_resp = requests.Response()
    initial_resp.status_code = 302
    initial_resp.headers['Location'] = '/retry'
    initial_resp.url = 'http://example.com/bad-chunk'
    initial_resp.request = initial_req
    
    # Setup mock raw to simulate broken stream
    mock_raw = Mock()
    # When resp.content is accessed, it iterates stream. Raise error there.
    mock_raw.stream.side_effect = ChunkedEncodingError("Connection broken")
    # Verify fallback read is allowed
    mock_raw.read.return_value = b""
    initial_resp.raw = mock_raw

    def send_side_effect(request, **kwargs):
        resp = requests.Response()
        resp.status_code = 200
        resp.url = request.url
        resp.request = request
        resp._content = b'ok'
        resp._content_consumed = True
        resp.raw = Mock()
        return resp

    with patch.object(session, 'send', side_effect=send_side_effect):
        gen = session.resolve_redirects(initial_resp, initial_req)
        
        # Triggering the generator executes the logic
        next(gen)
        
        # Assert fallback was called
        mock_raw.read.assert_called_with(decode_content=False)