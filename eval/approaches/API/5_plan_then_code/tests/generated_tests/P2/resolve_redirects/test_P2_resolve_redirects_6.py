import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_relative_url_normalization():
    """
    Test that a relative 'Location' header is correctly resolved to an absolute URL
    using the response URL as the base.
    """
    session = Session()
    
    base_url = 'http://example.com/subdir/resource'
    # Relative path in Location
    relative_target = '../new_resource'
    expected_target = 'http://example.com/new_resource'
    
    req = Request('GET', base_url).prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.url = base_url
    resp.headers['Location'] = relative_target
    resp._content = b''
    resp._content_consumed = True
    resp.request = req
    
    captured_requests = []
    def side_effect(request, **kwargs):
        captured_requests.append(request)
        r = Response()
        r.status_code = 200
        r.url = request.url
        r._content = b'OK'
        r._content_consumed = True
        return r
        
    session.send = Mock(side_effect=side_effect)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    sent_req = captured_requests[0]
    
    assert sent_req.url == expected_target