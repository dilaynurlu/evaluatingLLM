import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest

def test_resolve_redirects_relative_header():
    """
    Test that relative paths in the Location header are correctly joined
    with the original URL to form an absolute URL.
    """
    session = requests.Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/nested/path/resource')
    
    resp = Response()
    resp.status_code = 302
    # Relative path navigating up
    resp.headers['Location'] = '../../root'
    resp.url = 'http://example.com/nested/path/resource'
    resp.request = req
    resp._content = b''
    
    with patch.object(session, 'send', return_value=Response()) as mock_send:
        gen = session.resolve_redirects(resp, req)
        next(gen, None)
        
        sent_req = mock_send.call_args[0][0]
        
        # 'http://example.com/nested/path/resource' + '../../root'
        # Should resolve to 'http://example.com/root'
        assert sent_req.url == 'http://example.com/root'