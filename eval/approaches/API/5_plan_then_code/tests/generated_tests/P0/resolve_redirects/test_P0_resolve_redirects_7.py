import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_protocol_relative_url():
    """
    Test handling of protocol-relative URLs (starting with //).
    """
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='https://secure.example.com/start')
    
    resp1 = Response()
    resp1.status_code = 302
    resp1.headers['Location'] = '//cdn.example.com/resource'
    resp1.url = 'https://secure.example.com/start'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    captured_urls = []
    def send_mock(request, **kwargs):
        captured_urls.append(request.url)
        return Response() # Empty response to stop loop (no Location header)
        
    session.send = MagicMock(side_effect=send_mock)
    
    # We must mock get_redirect_target for the return value of send_mock to return None (stop loop)
    # The default Response() has no headers, so get_redirect_target returns None naturally.
    
    list(session.resolve_redirects(resp1, req))
    
    assert len(captured_urls) == 1
    # Should preserve 'https' scheme
    assert captured_urls[0] == 'https://cdn.example.com/resource'