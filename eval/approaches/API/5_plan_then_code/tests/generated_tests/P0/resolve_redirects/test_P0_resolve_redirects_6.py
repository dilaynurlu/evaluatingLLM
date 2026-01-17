import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_fragment_preservation():
    """
    Test that URL fragments are preserved or updated correctly during redirects.
    Case: Redirect Location has no fragment, so original fragment is preserved.
    """
    session = Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/page#original')
    
    resp1 = Response()
    resp1.status_code = 302
    # Location has NO fragment
    resp1.headers['Location'] = '/other'
    resp1.url = 'http://example.com/page'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    captured_urls = []
    def send_mock(request, **kwargs):
        captured_urls.append(request.url)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp._content = b""
        resp._content_consumed = True
        resp.raw = MagicMock()
        return resp
        
    session.send = MagicMock(side_effect=send_mock)
    
    list(session.resolve_redirects(resp1, req))
    
    assert len(captured_urls) == 1
    # Expect fragment to be preserved
    assert captured_urls[0] == 'http://example.com/other#original'